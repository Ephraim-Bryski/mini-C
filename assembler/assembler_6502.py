"""
honestly might be easier just to make my own emulator for writing tests
might even be nicer for debugging even then using platformio
you would debug the emulator to debug the assembly
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Dict
import re
import subprocess
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from instruction_set import *
import compiler.compiler as compiler


class LabelByte(Enum):
    ABSOLUTE_LOW = auto()
    ABSOLUTE_HIGH = auto()
    RELATIVE = auto()

@dataclass
class LabelPlaceholder:
    label: str
    type: LabelByte

@dataclass
class LabelAddress:
    """
    with org specification these two are different
    binary_idx: location in the binary, needed for branches
    absolute: absolute address
    """
    binary_idx: int
    absolute: int


class ADDRESS_STATE:
    binary: list[int] = []
    current_address: int = 0
    first_line: bool = True
    labels: Dict[str, LabelAddress] = {}
    aliases: Dict[str, int] = {}



class ValueException(Exception):...

def get_value(text):
    # Define a regex pattern to match text within single or double quotes
    quote_enclosed_regex = r'["\'](.*?)["\']'  # Matches text within ' or "

    def get_ascii_value(match):
        text_in_quotes = match.group(1)  # Extract the text within quotes
        return f'{ord(text_in_quotes)}'

    text = re.sub(quote_enclosed_regex, get_ascii_value, text)

    text = text.replace("%","0b")
    text = text.replace("$","0x")

    try:
        value = eval(text, ADDRESS_STATE.aliases)
    except:
        raise ValueException()

    return value




def clean_text(lines: list[str]):
    cleaned_lines = []
    for line in lines:
        line = line.replace("\n","")
        if ";" in line:
            comment_start = line.index(";")
            line = line[0:comment_start]
        if line.replace(" ","") == "":
            continue
        cleaned_lines.append(line)
    return cleaned_lines

def assemble_dotdir(line):

    first_space = line.index(" ")
    dot_mnemonic = line[1:first_space]
    parameter = line[first_space:].replace(" ","")
    
    match dot_mnemonic:
        case "asciiz":
            phrase = line[first_space+2:-1]
            ascii_binary = [ord(char) for char in phrase]
            ascii_binary.append(0)
            ADDRESS_STATE.binary += ascii_binary
            ADDRESS_STATE.current_address += len(ascii_binary)
        case "org":
            new_address = get_value(parameter)
            if not ADDRESS_STATE.first_line:
                old_address = ADDRESS_STATE.current_address
                fill = [0] * (new_address - old_address)
                ADDRESS_STATE.binary += fill

            ADDRESS_STATE.current_address = new_address
        case "word":
    
            # this ones a bit hacky
            # i also need .word to use labels for reset, nmi, irqb addresses
    
            try:
                word = get_value(parameter)
                word_low = word % 256
                word_high = int(word/256)
                word_bytes = [word_low, word_high]
            except(ValueException):
                word_bytes = [
                    LabelPlaceholder(parameter, LabelByte.ABSOLUTE_LOW),
                    LabelPlaceholder(parameter, LabelByte.ABSOLUTE_HIGH)
                ]

            ADDRESS_STATE.binary += word_bytes
            ADDRESS_STATE.current_address += len(word_bytes)


        case _: raise Exception(f"{dot_mnemonic} unknown")


def assemble_instruction(line: str):
    """
    basically i need to know both the address mode and the instruction 
    """




    parts = [part for part in line.split(" ") if part != ""]

    mnemonic = parts[0]

    parameter_text = "".join(parts[1:])

    # if len(parts) == 1:
    #     mnemonic = parts[0]
    #     parameter_text = ""
    # elif len(parts) == 2:
    #     (mnemonic, parameter_text) = parts
    # else: assert False

    mnemonic = mnemonic.lower()
    # i'll also assume accumulator has A at the end


    matched_instruction_types = [instruction_type for instruction_type in InstructionTypes if instruction_type.mnemonic == mnemonic]
    assert len(matched_instruction_types) == 1

    instruction_type = matched_instruction_types[0]
    possible_address_modes = list(instruction_type.op_codes.keys())


    address_mode: AddressMode
    parameters: list[int|LabelPlaceholder]

    if instruction_type.is_jump:
        assert AddressMode.Absolute in possible_address_modes, "shouldnt fail, jmp and jsr have absolute"
        address_mode = AddressMode.Absolute
        assert instruction_type.is_jump, "either should be a jump or should be have a parameter address"
        parameters = [
            LabelPlaceholder(parameter_text, LabelByte.ABSOLUTE_LOW),
            LabelPlaceholder(parameter_text, LabelByte.ABSOLUTE_HIGH),
        ]
    elif parameter_text in ADDRESS_STATE.labels.keys():
        assert [AddressMode.Relative] == possible_address_modes
        # this would be a branch instruction
        parameters = [LabelPlaceholder(parameter_text, LabelByte.RELATIVE)]
        address_mode = AddressMode.Relative
    elif parameter_text == "":
        if [AddressMode.Implied] == possible_address_modes:
            address_mode = AddressMode.Implied
        elif [AddressMode.Accumulator] == possible_address_modes:
            address_mode = AddressMode.Accumulator   
        else: assert False 
        parameters = []
    elif parameter_text.startswith("#"):
        assert AddressMode.Immediate in possible_address_modes
        immediate_value = get_value(parameter_text[1:])
        if immediate_value > 255: raise Exception("cant do an immediate load, too big")
        parameters = [immediate_value % 256]
        address_mode = AddressMode.Immediate
    else:
        x_offset_text = ",x"
        is_x_offset = parameter_text.lower().endswith(x_offset_text)
        y_offset_text = ",y"
        is_y_offset = parameter_text.lower().endswith(y_offset_text)

        if is_x_offset:
            value_text = parameter_text.replace(x_offset_text, "").replace(x_offset_text.upper(),"")
        elif is_y_offset:
            value_text = parameter_text.replace(y_offset_text, "").replace(y_offset_text.upper(),"")
        else:
            value_text = parameter_text

        # NOTE that this only works for indirect indexed, not indexed indirect
        is_indirect = value_text.startswith("(") and value_text.endswith(")")

        # this has to be referring to an address
        address_value = get_value(value_text)
        value_low = address_value % 256
        value_high = int(address_value/256)

        has_address_address_modes = \
            AddressMode.ZeroPage in possible_address_modes and \
            AddressMode.Absolute in possible_address_modes
        
        assert has_address_address_modes, "might be possible, but want to check what's going on"
        
        is_zero_page = value_high == 0

        if is_zero_page:
            parameters = [value_low]
        else:
            parameters = [value_low, value_high]

        is_non_offset = not is_x_offset and not is_y_offset

        if is_zero_page and is_x_offset: address_mode = AddressMode.ZeroPageX
        elif is_zero_page and is_y_offset and is_indirect: address_mode = AddressMode.IndirectIndexed
        elif is_zero_page and is_y_offset and not is_indirect: address_mode = AddressMode.ZeroPageY
        elif is_zero_page and is_non_offset: address_mode = AddressMode.ZeroPage
        elif not is_zero_page and is_x_offset: address_mode = AddressMode.AbsoluteX
        elif not is_zero_page and is_y_offset and is_indirect: raise Exception("indirect can only have 8 bit offset")
        elif not is_zero_page and is_y_offset and not is_indirect: address_mode = AddressMode.AbsoluteY
        elif not is_zero_page and is_non_offset: address_mode = AddressMode.Absolute
        else: assert False
        

    op_code = instruction_type.op_codes[address_mode]

    return [op_code]+parameters


def fill_in_label_placeholders():

    for (byte_idx, byte) in enumerate(ADDRESS_STATE.binary):
        if type(byte) is not LabelPlaceholder: continue
        
        label = byte.label
        
        if label == '_print_char':
            instruction_type_byte = ADDRESS_STATE.binary[byte_idx-1]
            assert instruction_type_byte == 32, "should only be doing jsr for _print_char"
            ADDRESS_STATE.binary[byte_idx-1] = PRINT_CHAR_BYTE
            ADDRESS_STATE.binary[byte_idx] = 0 # arbitrary
            assert type(ADDRESS_STATE.binary[byte_idx+1]) is LabelPlaceholder, "it should have two bytes since it's aboslute"
            ADDRESS_STATE.binary[byte_idx+1] = 0
            continue

        label_address = ADDRESS_STATE.labels[label]

        match byte.type:
            case LabelByte.ABSOLUTE_LOW:
                value = label_address.absolute % 256
            case LabelByte.ABSOLUTE_HIGH:
                value = int(label_address.absolute/256)
            case LabelByte.RELATIVE:
                next_instruction_location = byte_idx + 1
                value = label_address.binary_idx - next_instruction_location
                if value < -128 or value > 127:
                    raise Exception(f"branched too far away: {value}")
                if value < 0: value = 256 + value
            case _: assert False

        ADDRESS_STATE.binary[byte_idx] = value




output_filename = "my_a.out"

def assemble(raw_assembly, compare_with_vasm=True):
    
    
    raw_lines = raw_assembly.split("\n")
    lines = clean_text(raw_lines)

    for line in lines:
        if line.startswith(" "): continue
        line = line.replace(" ","")
        if not line.endswith(":"): continue
        label = line.replace(":","")
        ADDRESS_STATE.labels[label] = None

    for line in lines:
        if "=" in line:
            (alias, value_text) = line.replace(" ","").split("=")
            ADDRESS_STATE.aliases[alias] = get_value(value_text)
            continue



        is_label = not line.startswith(" ")

        if is_label:
            label_name = line.replace(":","").replace(" ","")
            assert label_name in ADDRESS_STATE.labels.keys(), "this is a real assertion this shouldn't happen"
            binary_idx = len(ADDRESS_STATE.binary)
            label_address = LabelAddress(binary_idx, ADDRESS_STATE.current_address)
            if ADDRESS_STATE.labels[label_name] is not None:
                raise Exception(f"{label_name} label in more than one location")
            ADDRESS_STATE.labels[label_name] =  label_address

        else:
            stripped_line = line.lstrip()
            if stripped_line[0] == ".":
                assemble_dotdir(stripped_line)
            else:
                instruction_binary = assemble_instruction(stripped_line)
                ADDRESS_STATE.binary += instruction_binary
                ADDRESS_STATE.current_address += len(instruction_binary)
            
        ADDRESS_STATE.first_line = False

    fill_in_label_placeholders()

    byte_array = bytes(ADDRESS_STATE.binary)

    with open(output_filename,"wb") as f:
        f.write(byte_array)
    
    
    if compare_with_vasm:

        vasm_binary = assemble_with_vasm(raw_assembly)

        if vasm_binary != byte_array:
            for idx, (vasm_byte, my_byte) in enumerate(zip(vasm_binary, byte_array)):
                if vasm_byte != my_byte:
                    print(idx, vasm_byte, my_byte)
                    break
            raise Exception("binary doesn't match vasm")

    return byte_array


        
def get_hex_string(value):
    return f'0x{value:02x}'




def assemble_with_vasm(assembly):
    
    # assembly_file = "from_github.s"
    assembly_file = "main.S"

    
    with open(assembly_file,"w") as f:
        f.write(assembly)



    # assembly_file = "mine.s"
    assemble_result = subprocess.run(\
        f"assembler/vasm6502_oldstyle {assembly_file} -Fbin -dotdir", \
        capture_output = True, text = True)

    # print(assemble_result.stdout)

    if assemble_result.returncode != 0:
        print(assemble_result.stderr)
        raise Exception("error in assembly")

    if assemble_result.stderr != '':
        print(assemble_result.stderr)
        raise Exception("warning in assembly")

    with open("a.out","rb") as f:
        binary = f.read()
    return binary


if __name__ == "__main__":
    raw_assembly = compiler.compile("c programs/test.c")
    with open("main.S","w") as f:
        f.write(raw_assembly)
    # with open("main.S") as f:
    #     raw_assembly = f.read()
    assemble(raw_assembly)

    print([get_hex_string(byte) for byte in ADDRESS_STATE.binary])