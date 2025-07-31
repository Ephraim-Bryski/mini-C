import serial
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assembler')))
import assembler_6502
# from assembler import assembler_6502
# import assembler.assembler_6502 as assembler_6502
import compiler.compiler as compiler

assert __name__ == "__main__"

def find_first_difference(a: bytes, b: bytes):
    for idx,(a_byte, b_byte) in enumerate(zip(a,b)):
        if a_byte != b_byte: return idx
    return -1

previous_binary_file_name = "previous_binary.bin"

try:
    with open(previous_binary_file_name, "rb") as f:
        previous_binary = f.read()
except:
    previous_binary = b''


# assembly = compiler.compile("main.c")
with open("main.S") as f:
    assembly = f.read()


binary_full = assembler_6502.assemble(assembly)

print("generated binary")

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

# if there's additional code it will realize the change
padded_previous_binary = previous_binary.ljust(len(binary_code))
start_difference_idx = find_first_difference(padded_previous_binary, binary_code)

if start_difference_idx == -1:
    print("no change from previous binary, nothing to flash")
    exit()


start_difference_low = start_difference_idx % 256
start_difference_high = int(start_difference_idx/256)





nmi_address_low = binary_full[nmi_location_low]
nmi_address_high = binary_full[nmi_location_high]

start_address_low = binary_full[start_location_low]
start_address_high = binary_full[start_location_high]

irqb_address_low = binary_full[irqb_location_low]
irqb_address_high = binary_full[irqb_location_high]


reset_interrupt_vectors = binary_full[nmi_location_low: irqb_location_high+1]

with serial.Serial('COM7', 57600, timeout = 0.1) as ser:
    
    # for some rea
    # son the first read fails
    

    size = len(binary_code)
    size_low = size % 256
    size_high = int(size/256)

    test_value = 50
    while True:
        ser.write(test_value.to_bytes())
        value = ser.read(1)
        if len(value) != 0:
            assert value[0] == test_value * 2
            break

    print('starting communication')

    ser.write(size_low.to_bytes())
    low_confirm = ser.read(1)
    assert low_confirm[0] == size_low

    ser.write(size_high.to_bytes())
    high_confirm = ser.read(1)
    assert high_confirm[0] == size_high

    ser.write(start_difference_low.to_bytes())
    low_confirm = ser.read(1)
    assert low_confirm[0] == start_difference_low

    ser.write(start_difference_high.to_bytes())
    high_confirm = ser.read(1)
    assert high_confirm[0] == start_difference_high


    print('sent size')

    WRITE_CONFIRM = 10
    
    assert len(reset_interrupt_vectors) == 6
    idx = 0
    while True:
        byte_to_send = reset_interrupt_vectors[idx]
        ser.write(byte_to_send.to_bytes())
        response = ser.read(1)
        if len(response) == 0: continue
        assert response[0] == byte_to_send
        print(idx, response)
        idx += 1
        if idx == 6: break

    print("sent vectors")

    idx = start_difference_idx
    while True:
        byte_to_send = binary_code[idx]
        ser.write(byte_to_send.to_bytes())
        response = ser.read(1)
        if len(response) == 0: continue
        assert response[0] == WRITE_CONFIRM
        idx += 1
        if idx % 100 == 0:
            print(f"{idx}/{size} written")
        if idx == size: break

    print("code wrote")

    idx = start_difference_idx
    while True:
        ser.write(b'g')
        line = ser.read(1)
        if len(line) == 0: continue
        actual_byte = line[0]
        target_byte = binary_code[idx]
        if actual_byte != target_byte:
            raise Exception("no match o:")
        idx += 1
        if idx == size: break
    
    print("code read, good to go :)")    



with open(previous_binary_file_name, "wb") as f:
    f.write(binary_code)