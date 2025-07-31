"""
this test is now done in my assembler
"""

import subprocess
import assembler.assembler_6502 as assembler_6502


assembly_file = "compiler/main.S"

assemble_result = subprocess.run(\
    f"./vasm6502_oldstyle {assembly_file} -Fbin -dotdir", \
    capture_output = True, text = True)

if assemble_result.returncode != 0:
    print(assemble_result.stderr)
    raise Exception("error in assembly")

if assemble_result.stderr != '':
    print(assemble_result.stderr)
    raise Exception("warning in assembly")



with open("a.out","rb") as f:
    vasm_output = f.read()


assembler_6502.assemble(assembly_file)

with open(assembler_6502.output_filename,"rb") as f:
    my_output = f.read()


if vasm_output == my_output:
    print("match :D")
else:
    for idx, (vasm_byte, my_byte) in enumerate(zip(vasm_output, my_output)):
        if vasm_byte != my_byte:
            print(idx, vasm_byte, my_byte)
    raise Exception("NO GOOD")
