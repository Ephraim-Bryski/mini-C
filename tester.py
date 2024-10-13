from dataclasses import dataclass
from typing import Union
from typing import Any
from emulator import emulate_assembly
import compiler
from importlib import reload



@dataclass
class Test_Case:
    file_name: str
    expected_result: Any

test_cases = [
    Test_Case("comments.c", 4),
    Test_Case("var_starts_with_number.c", compiler.LexException),
    Test_Case("unmatched_parentheses.c", compiler.ParseException),
    Test_Case("undeclared.c", compiler.UndefinedException),
    Test_Case("function_not_declared.c", compiler.UndefinedException),
    Test_Case("declared_twice.c", compiler.RepeatedDeclarationException),
    Test_Case("functions_same_name.c", compiler.RepeatedDeclarationException),
    Test_Case("parameter_mismatch.c", compiler.ArgumentMismatchException),
    Test_Case("pemdas.c",72),
    Test_Case("logic.c",10),
    Test_Case("else_if.c",60),
    Test_Case("continue_break.c",5),
    Test_Case("multiple_parameters.c", 7),
    Test_Case("fib_loop.c", 13),
    Test_Case("fib_recursion.c", 13),
    Test_Case("chars.c", ord('h')),
    Test_Case("string.c", ord('e')),
    Test_Case("type_mismatch.c", compiler.TypeException),
    Test_Case("while_loop.c", 8),
    Test_Case("comparators.c", 1),
    Test_Case("invalid_field.c", compiler.StructException),
    Test_Case("structs.c", 12),
    Test_Case("array.c", 2),
    Test_Case("output_struct.c", 5),
    Test_Case("call_and_field.c", 13),
    Test_Case("AOS.c", 70),
    Test_Case("SOS.c",4),
    Test_Case("SOA.c",9),
    Test_Case("struct_ref.c", 6),
    Test_Case("type_cast.c",8),
    Test_Case("sizeof.c",1),
    Test_Case("int_wrap.c",1),
    Test_Case("string_length.c", 5),
    Test_Case("globals.c", 130),
    Test_Case("string_literal_argument.c", ord('o')),
    Test_Case("concatenate.c", 100),
    Test_Case("free.c", 0)
]



 
green_text_code = '\033[92m'
red_text_code = '\033[91m'
end_formatting_code = '\033[0m'
        
n_failed = 0

for test in test_cases:
    try:
        reload(compiler)
        assembly = compiler.compile(f"tests/{test.file_name}")
        registers = emulate_assembly(assembly)
        final_output = registers[compiler.TEMP_REG]
        test_passed = final_output == test.expected_result
    except Exception as e:
        final_output = f"{type(e)}, {e}"
        # since im reloading the compiler, the actual objects are different
        # comparing the strings is a hack to fix this
        test_passed = str(type(e)) == str(test.expected_result)

    if test_passed:
        print(f"{test.file_name} passed")
    else:
        n_failed += 1
        print(f"\
{red_text_code}{test.file_name} FAILED!\n\t\
Expected: {test.expected_result}\n\t  \
Actual: {final_output}{end_formatting_code}\
")

print("\n")
if n_failed == 0:
    print(f"{green_text_code}All tests passed!{end_formatting_code}")
else:
    print(f"{red_text_code}{n_failed} tests failed. be better.{end_formatting_code}")