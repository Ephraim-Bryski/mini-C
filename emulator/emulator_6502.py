"""
honestly might be easier just to make my own emulator for writing tests
might even be nicer for debugging even then using platformio
you would debug the emulator to debug the assembly
"""

from dataclasses import dataclass
from typing import List
from enum import Enum, auto
from instruction_set import *
import assembler.assembler_6502 as assembler_6502
import sys

sys.path.append("emulator")
import lcd_controller
import compiler.compiler as compiler

# just a hack so the emulator knows when it's done
# for the actual computer i stick it in an infinite loop
# but i'll put a write to this address right before the loop so the emulator knows it's done
# this address doesn't connect to the hardware so it doesn't matter
# (i could have separate asm and binary for hardware vs. emulator but this is simpler i think)
HALT_ADDRESS = 0x4000
EMULATION_HALTED = False

@dataclass(frozen=True)
class _EaterArchitecture:
    RAM_HIGH: int = 0x3fff
    VIA_LOW: int = 0x6000
    # technically via is enabled until 0x7fff
    # address space repeats over every 16bits
    # but gonna keep things simpler and  only allow first 16 bits
    VIA_HIGH: int = 0x600f
    ROM_LOW: int = 0x8000
    # need ones for via mapping, 
EaterArchitecture = _EaterArchitecture()

@dataclass(frozen=True)
class _Architecture6502:
    STACK_LOWER_BOUND = 0x100
    STACK_UPPER_BOUND = 0x1ff
    NMI_LOW: int = 0xfffa
    NMI_HIGH: int = 0xfffb
    START_LOW: int = 0xfffc
    START_HIGH: int = 0xfffd
    IRQ_LOW: int = 0xfffe
    IRQ_HIGH: int = 0xffff

Architecture6502 = _Architecture6502()



@dataclass(frozen=True)
class _CompilerArchitecture:
    BP_ADDRESS_LOW = 0x0
    BP_ADDRESS_HIGH = 0x1
    GLOBAL_P_ADDRESS_LOW = 0x2
    GLOBAL_P_ADDRESS_HIGH = 0x3
    INTERNAL_HIGH = 0xff    # includes base pointer and global pointer address
    HEAP_LOW = 0x200
    HEAP_HIGH = 0x3fff

CompilerArchitecture = _CompilerArchitecture()



class _Flags:
    zero: bool = False
    carry: bool = False
    negative: bool = False
    decimal_mode: bool = False
    interrupt_disable: bool = False

class CPU_STATE:
    program_count: int = 0
    flags: _Flags = _Flags()
    stack_pointer: int = 0
    accumulator: int = 0
    X_register: int = 0
    Y_register: int = 0
    memory: list[int] = [0]*0xffff
    increment_program_count: bool = True

def get_indirect_indexed_address(indirect_address: int) -> int:
    offset = CPU_STATE.Y_register
    address_low = read_memory_address(indirect_address)
    address_high = read_memory_address(indirect_address+1)
    return address_high*256 + address_low + offset

def get_address_from_relative(relative_address: int) -> int:
    
    # branches are relative to the end of the instruction not the start, so i have to add two
    # always two since relative is always two bytes
    instruction_size = 2

    if relative_address >= 128:
        relative_address_signed = relative_address - 256
    else:
        relative_address_signed = relative_address

    return CPU_STATE.program_count + relative_address_signed + instruction_size


def load_by_address_type(address_mode: AddressMode, address: int):

    match address_mode:
        case AddressMode.Implied: assert False, "shouldn't be loading for implied"
        case AddressMode.Accumulator: 
            value = CPU_STATE.accumulator
        case AddressMode.Immediate:
            value = address
        case AddressMode.ZeroPage:
            assert address < 256
            value = read_memory_address(address)
        case AddressMode.ZeroPageX:
            assert address < 256
            value = read_memory_address(address + CPU_STATE.X_register)
        case AddressMode.ZeroPageY:
            assert address < 256
            value = read_memory_address(address + CPU_STATE.Y_register)
        case AddressMode.Absolute:
            assert address >= 256
            value = read_memory_address(address)
        case AddressMode.AbsoluteX:
            assert address >= 256
            value = read_memory_address(address + CPU_STATE.X_register)
        case AddressMode.AbsoluteY:
            assert address >= 256
            value = read_memory_address(address + CPU_STATE.Y_register)
        case AddressMode.IndirectIndexed:
            indirected_address = get_indirect_indexed_address(address)
            value = read_memory_address(indirected_address)
        case _: assert False
        
    return value

def store_by_address_type(address_mode: AddressMode, address: int, value: int):

    match address_mode:
        case AddressMode.Implied: assert False, "shouldn't be storing for implied"
        case AddressMode.Accumulator: assert False, "shouldn't be storing for accumulator"
        case AddressMode.Immediate: assert False, "shouldn't be storing for immediate"
        case AddressMode.ZeroPage:
            assert address < 256
            write(address, value)
        case AddressMode.ZeroPageX:
            assert address < 256
            write(address + CPU_STATE.X_register, value)
        case AddressMode.ZeroPageY:
            assert address < 256
            write(address + CPU_STATE.Y_register, value)
        case AddressMode.Absolute:
            assert address >= 256
            write(address, value)
        case AddressMode.AbsoluteX:
            assert address >= 256
            write(address + CPU_STATE.X_register, value)
        case AddressMode.AbsoluteY:
            assert address >= 256
            write(address + CPU_STATE.Y_register, value)
        case AddressMode.IndirectIndexed:
            indirected_address = get_indirect_indexed_address(address)
            write(indirected_address, value)
        case _: assert False

def _is_in_ram(address: int) -> bool:
    return address <= CompilerArchitecture.HEAP_HIGH

def _is_in_via_address_space(address: int) -> bool:
    return address >= EaterArchitecture.VIA_LOW and address <= EaterArchitecture.VIA_HIGH
        

    

def read_memory_address(address) -> int:
    if _is_in_ram(address):
        return CPU_STATE.memory[address]
    elif _is_in_via_address_space(address):
        # FUTURE this is done when checking if lcd is busy
        return 0
    else:
        raise Exception(f"cant read from {address}")

def write(address, value) -> None:
    if _is_in_ram(address):
        CPU_STATE.memory[address] = value
    elif _is_in_via_address_space(address):
        mapped_address = address - EaterArchitecture.VIA_LOW
        lcd_controller.send_signal_to_via(mapped_address, value)
    elif address == HALT_ADDRESS:
        global EMULATION_HALTED
        EMULATION_HALTED = True
    else:
        raise Exception(f'cant write to {address}')

def _push_stack(value):
    
    CPU_STATE.memory[CPU_STATE.stack_pointer] = value
    CPU_STATE.stack_pointer -= 1
    if CPU_STATE.stack_pointer < Architecture6502.STACK_LOWER_BOUND:
        raise Exception("stack overflow")

    

def _pop_stack(): 

    CPU_STATE.stack_pointer += 1

    if CPU_STATE.stack_pointer > Architecture6502.STACK_UPPER_BOUND:
        raise Exception("stack underflow, something's wrong with the compiler O:")
    
    return CPU_STATE.memory[CPU_STATE.stack_pointer]


def set_arithmetic_flags(full_value, affect_carry):
    byte_value = full_value % 256
    if affect_carry:
        CPU_STATE.flags.carry = full_value > 255
    CPU_STATE.flags.zero = byte_value == 0
    CPU_STATE.flags.negative = byte_value & 128 > 0
    # TODO still need to figure out overflow


def adc(address_mode: AddressMode, parameter: int):
    carry_bit = CPU_STATE.flags.carry
    accumulator = CPU_STATE.accumulator
    value_to_add = load_by_address_type(address_mode, parameter)
    full_sum = carry_bit + accumulator + value_to_add
    CPU_STATE.accumulator = full_sum % 256
    set_arithmetic_flags(full_sum, True)

def and_(address_mode: AddressMode, parameter: int):
    value_to_and = load_by_address_type(address_mode, parameter)
    anded_value = CPU_STATE.accumulator & value_to_and
    CPU_STATE.accumulator = anded_value
    set_arithmetic_flags(anded_value, False)


def asl(address_mode: AddressMode, parameter: int):
    value = load_by_address_type(address_mode, parameter)
    shifted_value_full = value << 1
    shifted_value = shifted_value_full % 256
    store_by_address_type(address_mode, parameter, shifted_value)
    # this should move the old bit 7 into the carry flag
    set_arithmetic_flags(shifted_value_full, True)


def bcc(address_mode: AddressMode, parameter: int):
    address_to_branch = get_address_from_relative(parameter)
    if not CPU_STATE.flags.carry:
        CPU_STATE.program_count = address_to_branch
        CPU_STATE.increment_program_count = False

def bcs(address_mode: AddressMode, parameter: int):
    address_to_branch = get_address_from_relative(parameter)
    if CPU_STATE.flags.carry:
        CPU_STATE.program_count = address_to_branch
        CPU_STATE.increment_program_count = False



def beq(address_mode: AddressMode, parameter: int):
    address_to_branch = get_address_from_relative(parameter)
    if CPU_STATE.flags.zero:
        CPU_STATE.program_count = address_to_branch
        CPU_STATE.increment_program_count = False

def bne(address_mode: AddressMode, parameter: int):
    address_to_branch = get_address_from_relative(parameter)
    if not CPU_STATE.flags.zero:
        CPU_STATE.program_count = address_to_branch
        CPU_STATE.increment_program_count = False

def cmp(address_mode: AddressMode, parameter: int):
    # TODO it says carry flag is set if A>=M  or M<=A
    # doesnt make sense to me since if they're equal the difference would just be 0
    # i would think it would be M<A
    value_to_compare = load_by_address_type(address_mode, parameter)
    set_arithmetic_flags(value_to_compare - CPU_STATE.accumulator, True)

def cld(address_mode: AddressMode, parameter: int):
    
    CPU_STATE.flags.decimal_mode = False

def cli(address_mode: AddressMode, parameter: int):
    CPU_STATE.flags.interrupt_disable = False
    
def clc(address_mode: AddressMode, parameter: int):
    CPU_STATE.flags.carry = False

def dex(address_mode: AddressMode, parameter: int):
    CPU_STATE.X_register -= 1
    assert CPU_STATE.X_register >= 0
    set_arithmetic_flags(CPU_STATE.X_register, False)

def inc(address_mode: AddressMode, parameter: int):
    value = load_by_address_type(address_mode, parameter)
    value += 1
    assert value < 256
    store_by_address_type(address_mode, parameter, value)
    set_arithmetic_flags(value, False)

def inx(address_mode: AddressMode, parameter: int):
    CPU_STATE.X_register += 1
    assert CPU_STATE.X_register < 256
    set_arithmetic_flags(CPU_STATE.X_register, False)


def iny(address_mode: AddressMode, parameter: int):
    CPU_STATE.Y_register += 1
    assert CPU_STATE.Y_register < 256
    set_arithmetic_flags(CPU_STATE.Y_register, False)

def jmp(address_mode: AddressMode, parameter: int):
    assert address_mode == AddressMode.Absolute
    CPU_STATE.program_count = parameter
    CPU_STATE.increment_program_count = False


def jsr(address_mode: AddressMode, parameter: int):
    # in reality it pushes one minus the program count but this is the simplest way to implement it
    instruction_size = 3    # known since it's only absolute
    program_count = CPU_STATE.program_count + instruction_size
    program_count_low = program_count % 256
    program_count_high = int(program_count/256)
    _push_stack(program_count_low)
    _push_stack(program_count_high)
    CPU_STATE.program_count = parameter
    CPU_STATE.increment_program_count = False

def lda(address_mode: AddressMode, parameter: int):
    CPU_STATE.accumulator = load_by_address_type(address_mode, parameter)
    set_arithmetic_flags(CPU_STATE.accumulator, False)


def ldx(address_mode: AddressMode, parameter: int):
    CPU_STATE.X_register = load_by_address_type(address_mode, parameter)
    set_arithmetic_flags(CPU_STATE.X_register, False)

def ldy(address_mode: AddressMode, parameter: int):
    CPU_STATE.Y_register = load_by_address_type(address_mode, parameter)
    set_arithmetic_flags(CPU_STATE.Y_register, False)

def nop(address_mode: AddressMode, parameter: int):
    pass

def ora(address_mode: AddressMode, parameter: int):
    value = load_by_address_type(address_mode, parameter)
    CPU_STATE.accumulator |= value
    set_arithmetic_flags(CPU_STATE.accumulator, False)

def pha(address_mode: AddressMode, parameter: int):
    _push_stack(CPU_STATE.accumulator)

def get_object_fields(object):
    return [field for field in vars(type(object)).keys() if not field.startswith("__")]
     

def php(address_mode: AddressMode, parameter: int):
    flag_names = get_object_fields(CPU_STATE.flags)
    for name in flag_names:
        flag_value = CPU_STATE.flags.__getattribute__(name)
        _push_stack(int(flag_value))

def pla(address_mode: AddressMode, parameter: int):
    CPU_STATE.accumulator = _pop_stack()
    set_arithmetic_flags(CPU_STATE.accumulator, False)


def plp(address_mode: AddressMode, parameter: int):
    flag_names = get_object_fields(CPU_STATE.flags)
    flag_names.reverse()
    for name in flag_names:
        flag_value = bool(_pop_stack())
        CPU_STATE.flags.__setattr__(name, flag_value)
        

def rol(address_mode: AddressMode, parameter: int):
    value = load_by_address_type(address_mode, parameter)
    shifted_value_full = value << 1
    shifted_value_full += CPU_STATE.flags.carry
    shifted_value = shifted_value_full % 256
    store_by_address_type(address_mode, parameter, shifted_value)
    # this should move the old bit 7 into the carry flag
    set_arithmetic_flags(shifted_value_full, True)

def rti(address_mode: AddressMode, parameter: int):
    raise Exception("not implementing interrupts")

def rts(address_mode: AddressMode, parameter: int):
    new_program_count_high = _pop_stack()
    new_program_count_low = _pop_stack()
    new_program_count = new_program_count_low + new_program_count_high*256
    CPU_STATE.program_count = new_program_count
    CPU_STATE.increment_program_count = False


def sbc(address_mode: AddressMode, parameter: int):
    carry_bit = CPU_STATE.flags.carry
    value_to_subtract = load_by_address_type(address_mode, parameter)
    full_sum = CPU_STATE.accumulator - value_to_subtract - (1-carry_bit)
    CPU_STATE.accumulator = full_sum % 256
    set_arithmetic_flags(full_sum, True)
    CPU_STATE.flags.carry = full_sum >= 0

def sec(address_mode: AddressMode, parameter: int):
    CPU_STATE.flags.carry = True

def sei(address_mode: AddressMode, parameter: int):
    CPU_STATE.flags.interrupt_disable = True

def sta(address_mode: AddressMode, parameter: int):
    store_by_address_type(address_mode, parameter, CPU_STATE.accumulator)

def stx(address_mode: AddressMode, parameter: int):
    store_by_address_type(address_mode, parameter, CPU_STATE.X_register)

def sty(address_mode: AddressMode, parameter: int):
    store_by_address_type(address_mode, parameter, CPU_STATE.Y_register)

def tax(address_mode: AddressMode, parameter: int):
    CPU_STATE.X_register = CPU_STATE.accumulator
    set_arithmetic_flags(CPU_STATE.X_register, False)

def tay(address_mode: AddressMode, parameter: int):
    CPU_STATE.Y_register = CPU_STATE.accumulator
    set_arithmetic_flags(CPU_STATE.Y_register, False)

def tsx(address_mode: AddressMode, parameter: int):
    CPU_STATE.X_register = CPU_STATE.stack_pointer % 256
    set_arithmetic_flags(CPU_STATE.X_register, False)


def txa(address_mode: AddressMode, parameter: int):
    CPU_STATE.accumulator = CPU_STATE.X_register
    set_arithmetic_flags(CPU_STATE.accumulator, False)

def txs(address_mode: AddressMode, parameter: int):
    CPU_STATE.stack_pointer = 0x100 + CPU_STATE.X_register

def tya(address_mode: AddressMode, parameter: int):
    CPU_STATE.accumulator = CPU_STATE.Y_register
    set_arithmetic_flags(CPU_STATE.accumulator, False)


def emulate_binary(binary):

 
    place_to_look_for_start_low = Architecture6502.START_LOW - EaterArchitecture.ROM_LOW
    place_to_look_for_start_high = Architecture6502.START_HIGH - EaterArchitecture.ROM_LOW

    start_location_low = binary[place_to_look_for_start_low]
    start_location_high = binary[place_to_look_for_start_high]

    start_location = start_location_low + start_location_high * 256


    CPU_STATE.program_count = start_location

    def find_instruction_type(instruction_byte):
        for instruction in InstructionTypes:
            for (address_mode, op_code) in instruction.op_codes.items():
                if op_code == instruction_byte:
                    return [instruction, address_mode]

        raise Exception(f"{instruction_byte} isn't a known opcode")
    
    while not EMULATION_HALTED:

        mapped_program_count = CPU_STATE.program_count - EaterArchitecture.ROM_LOW
        if mapped_program_count >= len(binary):
            raise Exception("reached end of program before halting")
        CPU_STATE.increment_program_count = True
        byte = binary[mapped_program_count]
        if byte == PRINT_CHAR_BYTE:
            char_to_print = CPU_STATE.memory[CPU_STATE.stack_pointer]
            # print(chr(char_to_print),end='')
            print(char_to_print, chr(char_to_print))
            instruction_size = AddressModeSizes[AddressMode.Absolute]
        else:
            [instruction, address_mode] = find_instruction_type(byte)
            instruction_size = AddressModeSizes[address_mode]
            parameter_size = instruction_size - 1
            mnemonic = instruction.mnemonic
            parameter_bytes = binary[mapped_program_count+1:mapped_program_count+1+parameter_size]
            parameter_value = sum(x*256**i for (i,x) in enumerate(parameter_bytes))
            if mnemonic == "and":
                function_name = "and_"
            else: function_name = mnemonic
            instruction_function = globals()[function_name]
            instruction_function(address_mode, parameter_value)
        if CPU_STATE.increment_program_count:
            CPU_STATE.program_count += instruction_size

    return CPU_STATE.accumulator

if __name__ == "__main__":
    assembly = compiler.compile("mini_test.c")
    # with open("test.S") as f:
    #     assembly = f.read()
    binary = assembler_6502.assemble(assembly, compare_with_vasm=False)
    result = emulate_binary(binary)
    print(lcd_controller.get_diplay())
    ...