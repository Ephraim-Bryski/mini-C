
import subprocess
import pyperclip

# assembly_file = "from_github.s"
assembly_file = "main.S"
# assembly_file = "mine.s"
assemble_result = subprocess.run(\
    f"./vasm6502_oldstyle {assembly_file} -Fbin -dotdir", \
    capture_output = True, text = True)

print(assemble_result.stdout)

if assemble_result.returncode != 0:
    print(assemble_result.stderr)
    raise Exception("error in assembly")

if assemble_result.stderr != '':
    print(assemble_result.stderr)
    raise Exception("warning in assembly")

with open("a.out","rb") as f:
    binary_full = f.read()

def get_hex_string(value):
    return f'0x{value:02x}'

eeprom_address_shift = 0x8000

nmi_location_low = 0xfffa - eeprom_address_shift
nmi_location_high = 0xfffb - eeprom_address_shift

start_location_low = 0xfffc - eeprom_address_shift
start_location_high = 0xfffd - eeprom_address_shift

irqb_location_low = 0xfffe - eeprom_address_shift
irqb_location_high = 0xffff - eeprom_address_shift


# i use the .org directory in the asm so the jumps get positioned in the top half of the memory (where the eeprom is mapped to)
# but this then cause the binary to start with 0x8000 0s
# so i have to remove them
binary_code = binary_full[0:nmi_location_low].rstrip(b'\x00')
hex_text_code = ", ".join([get_hex_string(byte) for byte in binary_code])

nmi_address_low = binary_full[nmi_location_low]
nmi_address_high = binary_full[nmi_location_high]

start_address_low = binary_full[start_location_low]
start_address_high = binary_full[start_location_high]

irqb_address_low = binary_full[irqb_location_low]
irqb_address_high = binary_full[irqb_location_high]


eeprom_programmer_code = f"""
byte data[] = 
{{{hex_text_code}}};
writeEEPROM({get_hex_string(nmi_location_low)}, {nmi_address_low});
writeEEPROM({get_hex_string(nmi_location_high)}, {nmi_address_high});
writeEEPROM({get_hex_string(start_location_low)}, {start_address_low});
writeEEPROM({get_hex_string(start_location_high)}, {start_address_high});
writeEEPROM({get_hex_string(irqb_location_low)}, {irqb_address_low});
writeEEPROM({get_hex_string(irqb_location_high)}, {irqb_address_high});

"""

print("program copied :)")
# print(eeprom_programmer_code)
pyperclip.copy(eeprom_programmer_code)
