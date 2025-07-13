from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict

# some arbitrary placeholder for the _print_char emulator instruction
PRINT_CHAR_BYTE = 255

class AddressMode(Enum):
    Implied = auto()
    Accumulator = auto()
    Immediate = auto()
    ZeroPage = auto()
    ZeroPageX = auto()
    ZeroPageY = auto()
    Absolute = auto()
    AbsoluteX = auto()
    AbsoluteY = auto()
    Relative = auto()
    IndirectIndexed = auto()


AddressModeSizes = {
    AddressMode.Implied: 1,
    AddressMode.Accumulator: 1,
    AddressMode.Immediate: 2,
    AddressMode.ZeroPage: 2,
    AddressMode.ZeroPageX: 2,
    AddressMode.ZeroPageY: 2,
    AddressMode.Absolute: 3,
    AddressMode.AbsoluteX: 3,
    AddressMode.AbsoluteY: 3,
    AddressMode.Relative: 2,
    AddressMode.IndirectIndexed: 2
}

@dataclass
class _InstructionType:
    mnemonic: str
    op_codes: Dict[AddressMode, int]
    # i need to know if it's a jump since for jumps i'm includiung a placeholder for the label
    # dont need to do the same for branches since they're the only one with relative address mode (and they only use relative)
    is_jump: bool = False



InstructionTypes: list[_InstructionType] = [
    _InstructionType("adc", {
        AddressMode.Immediate: 0x69,
        AddressMode.ZeroPage: 0x65,
        AddressMode.Absolute: 0x6d,
        AddressMode.IndirectIndexed: 0x71,
    }),
    _InstructionType("and", {
        AddressMode.Immediate: 0x29,
        AddressMode.ZeroPage: 0x25,
        AddressMode.Absolute: 0x2d,
        AddressMode.IndirectIndexed: 0x31
    }),
    _InstructionType("asl", {
        AddressMode.Accumulator: 0x0a
    }),
    _InstructionType("bcc", {
        AddressMode.Relative: 0x90,
    }),
    _InstructionType("bcs", {
        AddressMode.Relative: 0xb0
    }),
    _InstructionType("beq", {
        AddressMode.Relative: 0xf0,
    }),
    _InstructionType("bit", {
        AddressMode.ZeroPage: 0x24,
        AddressMode.Absolute: 0x2c
    }),
    _InstructionType("bne", {
        AddressMode.Relative: 0xd0
    }),
    _InstructionType("cmp", {
        AddressMode.Immediate: 0xc9,
        AddressMode.ZeroPage: 0xc5,
        AddressMode.ZeroPageX: 0xd5,
        AddressMode.Absolute: 0xcd,
        AddressMode.AbsoluteX: 0xdd,
        AddressMode.AbsoluteY: 0xd9,
        AddressMode.IndirectIndexed: 0xd1
    }),
    _InstructionType("cld", {
        AddressMode.Implied: 0xd8
    }),
    _InstructionType("cli", {
        AddressMode.Implied: 0x58
    }),
    _InstructionType("clc", {
        AddressMode.Implied: 0x18
    }),
    _InstructionType("dec", {
        AddressMode.ZeroPage: 0xc6,
        AddressMode.ZeroPageX: 0xd6,
        AddressMode.Absolute: 0xce,
        AddressMode.AbsoluteX: 0xde
    }),
    _InstructionType("dex", {
        AddressMode.Implied: 0xca
    }),
    _InstructionType("dey", {
        AddressMode.Implied: 0x88
    }),
    _InstructionType("inc", {
        AddressMode.ZeroPage: 0xe6,
        AddressMode.ZeroPageX: 0xf6,
        AddressMode.Absolute: 0xee,
        AddressMode.AbsoluteX: 0xfe
    }),
    _InstructionType("inx", {
        AddressMode.Implied: 0xe8
    }),
    _InstructionType("iny", {
        AddressMode.Implied: 0xc8
    }),
    _InstructionType("jmp", {
        AddressMode.Absolute: 0x4c,
    }, is_jump=True),
    _InstructionType("jsr", {
        AddressMode.Absolute: 0x20
    }, is_jump=True),
    _InstructionType("lda", {
        AddressMode.Immediate: 0xa9,
        AddressMode.ZeroPage: 0xa5,
        AddressMode.ZeroPageX: 0xb5,
        AddressMode.Absolute: 0xad,
        AddressMode.AbsoluteX: 0xbd,
        AddressMode.AbsoluteY: 0xb9,
        AddressMode.IndirectIndexed: 0xb1
    }),
    _InstructionType("ldx", {
        AddressMode.Immediate: 0xa2,
        AddressMode.ZeroPage: 0xa6,
        AddressMode.ZeroPageY: 0xb6,
        AddressMode.Absolute: 0xae,
        AddressMode.AbsoluteY: 0xbe
    }),
    _InstructionType("ldy", {
        AddressMode.Immediate: 0xa0,
        AddressMode.ZeroPage: 0xa4,
        AddressMode.ZeroPageX: 0xb4,
        AddressMode.Absolute: 0xac,
        AddressMode.AbsoluteX: 0xbc
    }),
    _InstructionType("nop", {
        AddressMode.Implied: 0xea
    }),
    _InstructionType("ora", {
        AddressMode.Immediate: 0x09,
        AddressMode.ZeroPage: 0x05,
        AddressMode.ZeroPageX: 0x15,
        AddressMode.Absolute: 0x0d,
        AddressMode.AbsoluteX: 0x1d,
        AddressMode.IndirectIndexed: 0x11
    }),
    _InstructionType("pha", {
        AddressMode.Implied: 0x48
    }),
    _InstructionType("php", {
        AddressMode.Implied: 0x08
    }),
    _InstructionType("pla", {
        AddressMode.Implied: 0x68
    }),
    _InstructionType("plp" , {
        AddressMode.Implied: 0x28
    }),
    _InstructionType("rol", {
        AddressMode.Accumulator: 0x2a, 
        AddressMode.ZeroPage: 0x26,
        AddressMode.ZeroPageX: 0x36,
        AddressMode.Absolute: 0x2e,
        AddressMode.AbsoluteX: 0x3e
    }),
    _InstructionType("ror", {
        AddressMode.Accumulator: 0x6a,
        AddressMode.ZeroPage: 0x66,
        AddressMode.ZeroPageX: 0x76,
        AddressMode.Absolute: 0x6e,
        AddressMode.AbsoluteX: 0x7e
    }),


    _InstructionType("rti", {
        AddressMode.Implied: 0x40
    }),
    _InstructionType("rts", {
        AddressMode.Implied: 0x60
    }),
    _InstructionType("sbc", {
        AddressMode.Immediate: 0xe9, 
        AddressMode.ZeroPage: 0xe5,
        AddressMode.ZeroPageX: 0xf5,
        AddressMode.Absolute: 0xed,
        AddressMode.AbsoluteX: 0xfd,
        AddressMode.IndirectIndexed: 0xf1
    }),
    _InstructionType("sec", {
        AddressMode.Implied: 0x38
    }),
    _InstructionType("sei", {
        AddressMode.Implied: 0x78
    }),
    _InstructionType("sta", {
        AddressMode.ZeroPage: 0x85,
        AddressMode.ZeroPageX: 0x95,
        AddressMode.Absolute: 0x8d,
        AddressMode.AbsoluteX: 0x9d, 
        AddressMode.AbsoluteY: 0x99,
        AddressMode.IndirectIndexed: 0x91
    }),
    _InstructionType("stx", {
        AddressMode.ZeroPage: 0x86,
        AddressMode.ZeroPageY: 0x96,
        AddressMode.Absolute: 0x8e,
    }),
    _InstructionType("sty", {
        AddressMode.ZeroPage: 0x84,
        AddressMode.ZeroPageX: 0x94,
        AddressMode.Absolute: 0x8c
    }),
    _InstructionType("tax", {
        AddressMode.Implied: 0xaa
    }),
    _InstructionType("tay", {
        AddressMode.Implied: 0xa8
    }),
    _InstructionType("tsx", {
        AddressMode.Implied: 0xba
    }),
    _InstructionType("txa", {
       AddressMode.Implied: 0x8a 
    }),
    _InstructionType("tya", {
        AddressMode.Implied: 0x98
    }),
    _InstructionType("txs", {
        AddressMode.Implied: 0x9a
    }),

]

