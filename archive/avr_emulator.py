"""
honestly might be easier just to make my own emulator for writing tests
might even be nicer for debugging even then using platformio
you would debug the emulator to debug the assembly
"""
from compiler_architecture import *


def emulate_assembly(assembly):

    def see_stack(size = 10):
        for offset in range(-size, 1):
            print(offset, MEMORY[__INITIAL_STACK_POINTER__+offset])

    def pprint():
        red_text_code = '\033[91m'
        end_formatting_code = '\033[0m'
        for idx, instruction in enumerate(instructions):
            if idx == PROGRAM_COUNT:
                print(f"{red_text_code}{instruction}{end_formatting_code}")
            else:
                print(instruction)



    PROGRAM_COUNT = 0



    # a bit of a cheat in reality there are flags for greater, less etc. but this is fine
    COMPARE_A = 0
    COMPARE_B = 0

    REGISTERS = {}
    for i in range(32):
        REGISTERS[f"r{i}"] = 0


    MEMORY = [0]*1000


    def get_low(word):
        return word % 256
    
    def get_high(word):
        return int(word/256)
    
    def get_word(low, high):
        return high*256 + low

    CARRY_FLAG = 0


    __INITIAL_STACK_POINTER__ = 255


    MEMORY[SP_ADDRESS_LOW] = get_low(__INITIAL_STACK_POINTER__)
    MEMORY[SP_ADDRESS_HIGH] = get_high(__INITIAL_STACK_POINTER__)



    def PUSH_STACK(value):
        
        stack_pointer = get_word(MEMORY[SP_ADDRESS_LOW], MEMORY[SP_ADDRESS_HIGH])
        MEMORY[stack_pointer] = value
        stack_pointer -= 1
        if stack_pointer < 0:
            raise Exception("stack overflow!!")
        MEMORY[SP_ADDRESS_LOW] = get_low(stack_pointer)
        MEMORY[SP_ADDRESS_HIGH] = get_high(stack_pointer)


    def POP_STACK(): 

        new_stack_pointer = get_word(MEMORY[SP_ADDRESS_LOW], MEMORY[SP_ADDRESS_HIGH]) + 1
        MEMORY[SP_ADDRESS_LOW] = get_low(new_stack_pointer)
        MEMORY[SP_ADDRESS_HIGH] = get_high(new_stack_pointer)
        if new_stack_pointer > __INITIAL_STACK_POINTER__:
            raise Exception("stack underflow, something's wrong with the compiler O:")
        return MEMORY[new_stack_pointer]

    instructions_with_markers = [instr for instr in assembly.split("\n") if instr != "" and instr[0] != ";"]
    marker_locations = {}
    instructions = []
    for line in instructions_with_markers:
        if line == ".global main":
            continue
        elif line[-1] == ":":
            marker = line[0:-1]
            marker_locations[marker] = len(instructions)
        else:
            instructions.append(line)

    original_registers = list(REGISTERS.keys())

    while True:

        if PROGRAM_COUNT == len(instructions):

            assert original_registers == list(REGISTERS.keys()),\
            "some register was created, maybe i forgot reg_name before the register number in the compiler?"

            return REGISTERS

        instruction = instructions[PROGRAM_COUNT]
        instruction = instruction.replace(","," ")
        parts = instruction.split(" ")

        parts = [part for part in parts if part != ""]
        command = parts[0]

        increment_pc = True

        if command == "ldi":
            source = parts[2]
            destination = parts[1]
            assert destination in REGISTERS.keys()
            REGISTERS[destination] = int(source)
        elif command == "mov":
            source = parts[2]
            destination = parts[1]
            assert source in REGISTERS.keys()
            assert destination in REGISTERS.keys()
            REGISTERS[destination] = REGISTERS[source]
        elif command == "addi":
            op1 = REGISTERS[parts[1]]
            op2 = int(parts[2])
            result = op1 + op2
            REGISTERS[parts[1]] = get_low(result)
            CARRY_FLAG = int(result > 255)
        elif command == "adci":
            op1 = REGISTERS[parts[1]]
            op2 = int(parts[2])
            result = op1 + op2 + CARRY_FLAG
            REGISTERS[parts[1]] = get_low(result)
            CARRY_FLAG = int(result > 255)
        elif command == "add":
            op1 = REGISTERS[parts[1]]
            op2 = REGISTERS[parts[2]]
            result = op1 + op2
            REGISTERS[parts[1]] = get_low(result)
            CARRY_FLAG = int(result > 255)
        elif command == "adc":
            op1 = REGISTERS[parts[1]]
            op2 = REGISTERS[parts[2]]
            result = op1 + op2 + CARRY_FLAG
            REGISTERS[parts[1]] = get_low(result)
            CARRY_FLAG = int(result > 255)
        elif command == "sub":
            op1 = REGISTERS[parts[1]]
            op2 = REGISTERS[parts[2]] 
            result = op1 - op2
            REGISTERS[parts[1]] = get_low(result)
            CARRY_FLAG = int(result < 0)
        elif command == "sbc":
            op1 = REGISTERS[parts[1]]
            op2 = REGISTERS[parts[2]]
            result = op1 - op2 - CARRY_FLAG
            REGISTERS[parts[1]] = get_low(result)
            CARRY_FLAG = int(result < 0)
        elif command == "subi":
            op1 = REGISTERS[parts[1]]
            op2 = int(parts[2])
            result = op1 - op2
            REGISTERS[parts[1]] = get_low(result)
            CARRY_FLAG = int(result < 0)
        elif command == "sbci":
            op1 = REGISTERS[parts[1]]
            op2 = int(parts[2])
            result = op1 - op2 - CARRY_FLAG
            REGISTERS[parts[1]] = get_low(result)
            CARRY_FLAG = int(result < 0)
        elif command == "clc":
            CARRY_FLAG = 0
        elif command == "brcs":
            location = parts[1]
            if CARRY_FLAG:
                PROGRAM_COUNT = marker_locations[location]
                increment_pc = False
        elif command == "brcc":
            location = parts[1]
            if not CARRY_FLAG:
                PROGRAM_COUNT = marker_locations[location]
                increment_pc = False
        elif command == "mul":
            op1 = REGISTERS[parts[1]]
            op2 = REGISTERS[parts[2]]
            product = op1 * op2
            product_low = get_low(product)
            product_high = get_high(product)
            REGISTERS["r0"] = product_low
            REGISTERS["r1"] = product_high
        elif command == "jmp":
            assert len(parts) == 2
            destination = parts[1]
            PROGRAM_COUNT = marker_locations[destination]
            increment_pc = False
        elif command == "cpi":
            variable = parts[1]
            value = parts[2]
            assert variable in REGISTERS.keys()
            COMPARE_A = REGISTERS[variable]
            COMPARE_B = int(value)
        elif command == "cp":
            variable = parts[1]
            variable_2 = parts[2]
            assert variable in REGISTERS.keys()
            assert variable_2 in REGISTERS.keys()
            COMPARE_A = REGISTERS[variable]
            COMPARE_B = REGISTERS[variable_2]
        elif command == "breq":
            location = parts[1]
            if COMPARE_A == COMPARE_B:
                PROGRAM_COUNT = marker_locations[location]
                increment_pc = False
        elif command == "brne":
            location = parts[1]
            if COMPARE_A != COMPARE_B:
                PROGRAM_COUNT = marker_locations[location]
                increment_pc = False
        elif command == "brlo":
            location = parts[1]
            if COMPARE_A < COMPARE_B:
                PROGRAM_COUNT = marker_locations[location]
                increment_pc = False
        elif command == "brsh":
            location = parts[1]
            if COMPARE_A >= COMPARE_B:
                PROGRAM_COUNT = marker_locations[location]
                increment_pc = False
        elif command == "push":
            variable = parts[1]
            value = REGISTERS[variable]
            PUSH_STACK(value)
        elif command == "pop":
            variable = parts[1]
            REGISTERS[variable] = POP_STACK()
        elif command == "call":
            marker = parts[1]
            # technically it stores the pc+2 to get the next instruction
            # cause call is 32bits (twice as long as a normal instruction)
            # (cause it needs to store the full address o0f the instruction to go to)
            # it doesnt matter here though
            next_pc = PROGRAM_COUNT + 1
            next_pc_low = get_low(next_pc)
            next_pc_high = get_high(next_pc)
            PUSH_STACK(next_pc_low)
            PUSH_STACK(next_pc_high)
            PROGRAM_COUNT = marker_locations[marker]
            increment_pc = False
        elif command == "ret":
            pc_high = POP_STACK()
            pc_low = POP_STACK()
            PROGRAM_COUNT = pc_high*256 + pc_low
            increment_pc = False
        elif command == "lds":
            destination = parts[1]
            source = parts[2]
            REGISTERS[destination] = MEMORY[int(source)]
        elif command == "sts":
            destination = parts[1]
            source = parts[2]
            MEMORY[int(destination)] = REGISTERS[source]
        elif command == "ld":
            destination = parts[1]
            load_type = parts[2]
            if load_type != "X": raise Exception("for now just X loads allowed")
            address_low = REGISTERS[X_LOW]
            address_high = REGISTERS[X_HIGH]
            address = address_high*256 + address_low
            REGISTERS[destination] = MEMORY[int(address)]

        elif command == "ldd":
            destination = parts[1]
            load_type_with_offset = parts[2].replace(" ","")
            [load_type, offset] = load_type_with_offset.split("+")
            offset = int(offset)
            if load_type != "X": raise Exception("for now just X loads allowed")
            address_low = REGISTERS[X_LOW]
            address_high = REGISTERS[X_HIGH]
            address = address_high*256 + address_low
            REGISTERS[destination] = MEMORY[address+offset]

        elif command == "st":
            load_type = parts[1]
            source = parts[2]
            if load_type != "X": raise Exception("for now just X loads allowed")
            address_low = REGISTERS[X_LOW]
            address_high = REGISTERS[X_HIGH]
            address = address_high*256 + address_low
            MEMORY[address] = REGISTERS[source]
        elif command == "std":
            load_type_with_offset = parts[1].replace(" ","")
            [load_type, offset] = load_type_with_offset.split("+")
            offset = int(offset)
            source = parts[2]
            if load_type != "X": raise Exception("for now just X loads allowed")
            address_low = REGISTERS[X_LOW]
            address_high = REGISTERS[X_HIGH]
            address = address_high*256 + address_low
            MEMORY[address+offset] = REGISTERS[source]
        elif command == "_print_int8":
            stack_pointer = get_word(MEMORY[SP_ADDRESS_LOW], MEMORY[SP_ADDRESS_HIGH])
            print(MEMORY[stack_pointer+1], end="")
        elif command == "_print_int16":
            stack_pointer = get_word(MEMORY[SP_ADDRESS_LOW], MEMORY[SP_ADDRESS_HIGH])
            high_byte = MEMORY[stack_pointer+1]
            low_byte = MEMORY[stack_pointer+2]
            print(high_byte*256+low_byte, end="")
        elif command == "_print_char":
            stack_pointer = get_word(MEMORY[SP_ADDRESS_LOW], MEMORY[SP_ADDRESS_HIGH])
            print(chr(MEMORY[stack_pointer+1]), end="")
        else:
            raise Exception(f"unknown command: {command}")
        
        if increment_pc:
            PROGRAM_COUNT += 1
        

if __name__ == "__main__":
    from compiler import compile
    import sys

    if len(sys.argv) == 1:
        file_name = "test.c"
    else:
        file_name = sys.argv[1]  # Skip the first argument which is the script name

    assembly = compile(file_name)
    registers = emulate_assembly(assembly)
    print(f"\nr29: {registers['r29']}") 

