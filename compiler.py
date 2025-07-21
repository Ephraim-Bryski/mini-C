"""
goal

c compiler
in the end write in c instead 
make it bootstrap

dont care about efficiency at all

compile to avr assembly

for now just int datatype


"""


#
OFFSET_TEST = 200


from typing import Any
import os
from dataclasses import dataclass
from enum import Enum, auto
from typing import Union
from compiler_architecture import *
# REFACTOR
# i probably want a struct for each of these (chartokens, twochartokens, optokens etc)
# then the individual ones (equal, semicolon, comma etc.) would be enum values
# no, probably an array of structs



# really just so the tester can find what type of exception happened
class PreProcessException(Exception): pass
class LexException(Exception): pass
class ParseException(Exception): pass
class TypeException(Exception): pass
# just called for repeated declaration
# also for functions declared multiple times?
# im anyway going to be putting on the stack instead of registers in the future
# so it would just be repeated declarations
class RepeatedDeclarationException(Exception): pass
class UndefinedException(Exception): pass
class ArgumentMismatchException(Exception): pass

class NotImplementedYetException(Exception): pass

# maybe these should also be type exceptions?
class StructException(Exception): pass




def get_include_filename(line: str) -> str:

    broken_lines = line.split("#")

    if len(broken_lines) > 2:
        raise PreProcessException("cant have multiple pounds in a line")
    
    assert len(broken_lines) == 2, "should only be called if there's a pound"

    [white_spaces, include_text] = broken_lines

    if not include_text.startswith("include"):
        raise PreProcessException("only have include for preprocessing now")
    
    file_string = include_text.replace("include","",1)

    file_string_broken = file_string.split('"')

    if len(file_string_broken) != 3:
        raise PreProcessException(f"{file_string} is not a string to include")
    
    [_, file_name, _] = file_string_broken

    return file_name


included_files: list[str] = []

def preprocess(characters: str, previous_files: list[str], directory: list[str] = []) -> str:
        
    lines = characters.split("\n")

    new_lines: list[str] = []

    for line in lines:

        line = line.split("//")[0]
        if "#" not in line:
            new_lines.append(line)
            continue
        

        is_standard_include = "<" in line and ">" in line
        if is_standard_include:
            continue

        file_path = get_include_filename(line)

        relative_path_parts = file_path.split("/")

        absolute_path_parts = directory + relative_path_parts

        absolute_path = "/".join(absolute_path_parts)

        absolute_directory_parts = absolute_path_parts[0:-1]

        if absolute_path in previous_files:
            raise PreProcessException(f"circular dependencies found with {absolute_path}")
        

        if absolute_path in included_files:
            continue

        included_files.append(absolute_path)

        if not os.path.isfile(absolute_path):
            raise PreProcessException(f"'{absolute_path}' does not exist")

        with open(absolute_path) as f:
            raw_code = f.read()

        preprocessed_code = preprocess(raw_code, previous_files + [absolute_path], absolute_directory_parts)

        new_lines += preprocessed_code.split("\n")


    return "\n".join(new_lines)




CHAR_TOKENS: list[type] = []
TWO_CHAR_TOKENS: list[type] = []
OP_TOKENS: list[type] = []


ASSIGNMENT_TOKENS: list[type] = []

class EQUAL: char = "="
CHAR_TOKENS.append(EQUAL)
ASSIGNMENT_TOKENS.append(EQUAL)

class SEMICOLON: char = ";"
CHAR_TOKENS.append(SEMICOLON)  

class COMMA: char = ","
CHAR_TOKENS.append(COMMA)

class REFERENCE: char = "&"
CHAR_TOKENS.append(REFERENCE)

class SINGLE_QUOTE: char = "'"

class DOUBLE_QUOTE: char = '"'



class OR:
    chars = "||"
    order_weight = -2
TWO_CHAR_TOKENS.append(OR)
OP_TOKENS.append(OR)

class AND:
    chars = "&&"
    order_weight = -1
TWO_CHAR_TOKENS.append(AND)
OP_TOKENS.append(AND)



class LESS_THAN:
    char = "<"
    order_weight = 0
CHAR_TOKENS.append(LESS_THAN)
OP_TOKENS.append(LESS_THAN)

class GREATER_THAN:
    char = ">"
    order_weight = 0
CHAR_TOKENS.append(GREATER_THAN)
OP_TOKENS.append(GREATER_THAN)

class LESS_EQUAL:
    chars = "<="
    order_weight = 0
TWO_CHAR_TOKENS.append(LESS_EQUAL)
OP_TOKENS.append(LESS_EQUAL)

class GREATER_EQUAL:
    chars = ">="
    order_weight = 0
TWO_CHAR_TOKENS.append(GREATER_EQUAL)
OP_TOKENS.append(GREATER_EQUAL)


class EQUAL_COMPARE:
    chars = "=="
    order_weight = 0
TWO_CHAR_TOKENS.append(EQUAL_COMPARE)
OP_TOKENS.append(EQUAL_COMPARE)


class NOT_EQUAL:
    chars = "!="
    order_weight = 0
TWO_CHAR_TOKENS.append(NOT_EQUAL)
OP_TOKENS.append(NOT_EQUAL)

class PLUS_EQUAL:
    chars = "+="
TWO_CHAR_TOKENS.append(PLUS_EQUAL)
ASSIGNMENT_TOKENS.append(PLUS_EQUAL)

class MINUS_EQUAL:
    chars = "-="
TWO_CHAR_TOKENS.append(MINUS_EQUAL)
ASSIGNMENT_TOKENS.append(MINUS_EQUAL)

class TIMES_EQUAL:
    chars = "*="
TWO_CHAR_TOKENS.append(TIMES_EQUAL)
ASSIGNMENT_TOKENS.append(TIMES_EQUAL)

class FIELD_REFERENCE:
    chars = "->"
TWO_CHAR_TOKENS.append(FIELD_REFERENCE)




class PLUS:
    char = "+"
    order_weight = 1
CHAR_TOKENS.append(PLUS)
OP_TOKENS.append(PLUS)

class MINUS:
    char = "-"
    order_weight = 1
CHAR_TOKENS.append(MINUS)
OP_TOKENS.append(MINUS)

# FUTURE c using asterisk for multiply and pointers and pointer dereference could be an issue
# i think multiply vs dereference is just whether there's a number or variable before
    # yes -> multiply
    # no -> dereference
class ASTERISK:
    char = "*"
    order_weight = 2
CHAR_TOKENS.append(ASTERISK)
OP_TOKENS.append(ASTERISK)

class DIVIDE:
    char = "/"
    order_weight = 2
CHAR_TOKENS.append(DIVIDE)
OP_TOKENS.append(DIVIDE)

class BIT_OR:
    char = "|"
    order_weight = 3
CHAR_TOKENS.append(BIT_OR)
OP_TOKENS.append(BIT_OR)

class BIT_AND:
    char = "&"
    order_weight = 4
CHAR_TOKENS.append(BIT_AND)
OP_TOKENS.append(BIT_AND)

class NOT: char = "!"
CHAR_TOKENS.append(NOT)

class DOT: char = "."
CHAR_TOKENS.append(DOT)

class OPEN_PAREN: char = "("
CHAR_TOKENS.append(OPEN_PAREN)

class CLOSED_PAREN: char = ")"
CHAR_TOKENS.append(CLOSED_PAREN)

class OPEN_BRACKET: char = "["
CHAR_TOKENS.append(OPEN_BRACKET)

class CLOSED_BRACKET: char = "]"
CHAR_TOKENS.append(CLOSED_BRACKET)

class OPEN_CURLY: char = "{"
CHAR_TOKENS.append(OPEN_CURLY)

class CLOSED_CURLY: char = "}"
CHAR_TOKENS.append(CLOSED_CURLY)

open_tokens = [OPEN_PAREN, OPEN_BRACKET, OPEN_CURLY]
closed_tokens = [CLOSED_PAREN, CLOSED_BRACKET, CLOSED_CURLY]


KEYWORD_TOKENS: list[type] = []

class NULL_KEYWORD: keyword = "NULL"
KEYWORD_TOKENS.append(NULL_KEYWORD)

class IF_KEYWORD: keyword = "if"
KEYWORD_TOKENS.append(IF_KEYWORD)

class ELSE_KEYWORD: keyword = "else"
KEYWORD_TOKENS.append(ELSE_KEYWORD)

class FOR_KEYWORD: keyword = "for"
KEYWORD_TOKENS.append(FOR_KEYWORD)

class WHILE_KEYWORD: keyword = "while"
KEYWORD_TOKENS.append(WHILE_KEYWORD)

class CONTINUE_KEYWORD: keyword = "continue"
KEYWORD_TOKENS.append(CONTINUE_KEYWORD)

class BREAK_KEYWORD: keyword = "break"
KEYWORD_TOKENS.append(BREAK_KEYWORD)

class RETURN_KEYWORD: keyword = "return"
KEYWORD_TOKENS.append(RETURN_KEYWORD)

class STRUCT_KEYWORD: keyword = "struct"
KEYWORD_TOKENS.append(STRUCT_KEYWORD)


class Base_Types(Enum):
    # this is literally just so sizeof will get the total size of the array
    ARRAY_PLACEHOLDER = auto()
    STRING_PLACEHOLDER = auto()

    INT8 = auto()
    INT16 = auto()

PLACEHOLDER_TYPES = [Base_Types.ARRAY_PLACEHOLDER, Base_Types.STRING_PLACEHOLDER]



@dataclass
class VARIABLE:
    name: str
    def __repr__(self):
        return self.name

@dataclass
class NUMBER:
    # for now just ints
    value: int
    def __repr__(self):
        return str(self.value)



@dataclass
class CHAR:
    value: str
    def __repr__(self):
        return self.value

@dataclass
class STRING:
    value: str

Token = Union[Base_Types|NUMBER|VARIABLE|CHAR|STRING|SEMICOLON|COMMA]


def lex_alpha_num(chars: list[str]) -> Token:

    # for now no floats, so no decimals
    text = "".join(chars)

    for token in KEYWORD_TOKENS:
        if token.keyword == text:
            return token()

    # i'm not doing any fancy introspection on Types since i won't be able to when i bootstrap
    
    if text == "char":
        return Base_Types.INT8
    elif text == "int":
        return Base_Types.INT16

    if text.startswith("0b"):
        # removing the underscores so i can do stuff like 10_01_11_10 (easier to read)
        binary_number = text[2:].replace("_","")
        try:
            value = int(binary_number, 2)
        except:
            raise LexException(f"{binary_number} is an invalid binary number")
        return NUMBER(value)
    
    if text.startswith("0x"):
        hex_number = text[2:]
        try:
            value = int(hex_number, 16)
        except:
            raise LexException(f"{hex_number} is an invalid hexadecimal number")
        return NUMBER(value)
    

    starts_with_number = chars[0].isnumeric()
    number_chars = list(filter(lambda x:(x.isnumeric()), chars))
    is_all_numbers = len(number_chars) == len(chars)

    if is_all_numbers:
        return NUMBER(int("".join(chars)))

    if starts_with_number:
        raise LexException(f"var cannot start with number: {''.join(chars)}")
    
    return VARIABLE("".join(chars))

def lex_text(characters: str) -> list[Token]:

    is_in_alpha_num = False
    alpha_num_group = []
    tokens: list[Token] = []
    # characters = characters.replace("\n","")
    char_idx = 0


    while char_idx < len(characters):

        char_jump = 1
        is_valid_char = False
        is_special_two_char = False

        char = characters[char_idx]
        
        if char_idx+1 == len(characters):
            next_char = None
        else:
            next_char = characters[char_idx+1]

        is_alpha_num_char = char.isalnum() or char == "_"

        if char == "\n":
            is_valid_char = True
    


        if is_alpha_num_char:
            is_in_alpha_num = True
            is_valid_char = True
            alpha_num_group.append(char)
        elif is_in_alpha_num:
            is_in_alpha_num = False
            tokens.append(lex_alpha_num(alpha_num_group))
            alpha_num_group = []

        if char == SINGLE_QUOTE.char:
            is_valid_char = True
            char_char_idx = char_idx + 1
            closing_char_idx = char_idx + 2
            if closing_char_idx == len(characters):
                raise LexException("no closing quote")
            closed_quote = characters[char_idx+2]
            if closed_quote != SINGLE_QUOTE.char:
                raise LexException("no closing quote")
            tokens.append(CHAR(characters[char_char_idx]))
            char_jump = 3

        if char == DOUBLE_QUOTE.char:
            is_valid_char = True

            start_string_idx = char_idx+1
            closing_quote_idx = char_idx+1
            while characters[closing_quote_idx] != DOUBLE_QUOTE.char:
                closing_quote_idx += 1
                if closing_quote_idx == len(characters):
                    raise LexException("no closing quote")
            string_tokens = characters[start_string_idx:closing_quote_idx]
            tokens.append(STRING(string_tokens))

            # plus 2 for the two quotes
            char_jump = len(string_tokens)+2

        for token in TWO_CHAR_TOKENS:
            if char == token.chars[0] and next_char == token.chars[1]:
                is_valid_char = True
                is_special_two_char = True
                tokens.append(token())
                char_jump = 2

        # this is just to know if the & is a reference or a bitwise and
        # REFACTOR really ugly and brittle, very likely im missing something
        # really should be done in parsing not lexing
        is_after_value = len(tokens) > 0 and type(tokens[-1]) in [NUMBER, VARIABLE, CLOSED_BRACKET, CHAR, STRING]

        for token in CHAR_TOKENS:

            if token is REFERENCE and is_after_value:
                continue
            if token is BIT_AND and not is_after_value:
                continue

            if is_special_two_char: break
            if char == token.char:

                is_valid_char = True



                tokens.append(token())

        if char == " ":
            is_valid_char = True

        if not is_valid_char:
            raise LexException(f"char is not yet valid: {char}")
            
        char_idx += char_jump

    # if there's an alphanum at the very end (yes that will be a parse error, but it's not a lex error)
    if len(alpha_num_group) > 0:
        tokens.append(lex_alpha_num(alpha_num_group))

    return tokens




def find_matching_brace(tokens: list[Token], token_index: int) -> int:
    
    brace_token = tokens[token_index]
    brace_type = type(brace_token)

    if brace_type in open_tokens:
        matching_token_type = closed_tokens[open_tokens.index(brace_type)]
        deeper_token_group = open_tokens
        shallower_token_group = closed_tokens
        step = 1
    elif brace_type in closed_tokens:
        matching_token_type = open_tokens[closed_tokens.index(brace_type)]
        deeper_token_group = closed_tokens
        shallower_token_group = open_tokens
        step = -1
    else:
        assert False, "invalid token to find match"
    
    depth = 0

    while True:
        
        if token_index < 0 or token_index == len(tokens):
            raise ParseException("cant find matching brace")
        
        token = tokens[token_index]
        if type(token) in deeper_token_group:
            depth += 1
        elif type(token) in shallower_token_group:
            depth -= 1

        is_match = type(token) is matching_token_type
        if depth == 0 and is_match:
            return token_index
        if depth < 0:
            raise ParseException("brace mismatch")
        token_index += step




@dataclass
class Struct_Type:
    name: str

@dataclass
class Type:
    base_type: Union[Base_Types,Struct_Type]
    reference_level: int


@dataclass
class Variable_Typed:
    name: str
    type: Type


@dataclass
class Type_Cast:
    node: Any
    casted_type: Type


@dataclass
class Reference:
    variable_name: str

@dataclass
class Struct_Field:
    struct_node: Any
    field_name: str

@dataclass
class Array_Index:
    array: Any
    index: Any # FUTURE have a union type for an expression (variable, number, operation)


@dataclass
class Assignment:
    target: Any
    RHS: Any

@dataclass
class Declaration:
    target: Variable_Typed
    RHS: Any

@dataclass
class Return:
    value: Any

@dataclass
class Operation:
    operand1: Any
    operation: Any
    operand2: Any

@dataclass
class UnitaryOperation:
    operand: Any
    operation: Any

@dataclass
class Function_Call:
    function_name: str
    arguments: list

@dataclass
class If_Block:
    condition: Operation
    block: Any

@dataclass
class If_Container:
    blocks: list[If_Block]

@dataclass
class For_Block:
    initializer: Assignment
    condition: Operation
    incrementer: Assignment
    block: Any

@dataclass
class While_Block:
    condition: Operation
    block: Any

@dataclass
class Function_Block:
    output_type: Type
    name: str
    parameters: list[Variable_Typed]
    block: Any

@dataclass
class Struct:
    name: str
    # i need n_fields for bootstrapping (i wont know the array lengths)
    n_fields: int
    fields: list[Variable_Typed]


@dataclass
class Array_Literal:
    # i need n_items for bootstrapping (i wont know the array lengths)
    n_items: int
    items: list[Any]



def get_type(type_tokens:list) -> Type:

    if len(type_tokens) == 0:
        raise ParseException("no type specified")

    found_base_type = False
    n_pointers = 0
    is_struct = False

    for token_idx, token in enumerate(type_tokens):

        if token_idx == 0 and type(token) is STRUCT_KEYWORD:
            is_struct = True
            continue

        if not found_base_type:

            if not is_struct and type(token) is not Base_Types:
                raise ParseException()
            
            if is_struct:
                if type(token) is not VARIABLE:
                    raise ParseException(f"{token} is not valid for a struct num")
                base_type = Struct_Type(token.name)
            else:
                base_type = token

            found_base_type = True
            continue

        if type(token) is not ASTERISK:
            raise ParseException()
        
        n_pointers += 1

            
    return Type(base_type, n_pointers)        




def get_typed_variable(tokens: list) -> Variable_Typed:
    
    variable_token = tokens[-1]
    type_tokens = tokens[0:-1]
    if type(variable_token) is not VARIABLE:
        raise ParseException("")
    
    variable_type = get_type(type_tokens)

    return Variable_Typed(variable_token.name, variable_type)




    
Block = Union[For_Block|While_Block|If_Container|Function_Block]

Tree = Union[
    Token|
    Variable_Typed|
    Type_Cast|
    Reference|
    Operation|
    UnitaryOperation|
    Array_Index|
    Function_Call|
    Array_Literal|
    Return|
    Assignment|
    Declaration|
    Struct_Field|
    Block|
    list    # really a list[Tree] but i cant self reference
]



def parse_if_else_blocks(tokens: list[Token], start_index: int):

    # some of it will be redundant to parseblock, but id rather isolate it here

    assert type(tokens[start_index]) is IF_KEYWORD

    if_blocks: list[If_Block] = []

    reached_else = False

    while True:

        start_type = type(tokens[start_index])
        if  start_type is IF_KEYWORD:
            open_parentheses_index =  start_index + 1
            if type(tokens[open_parentheses_index]) is not OPEN_PAREN:
                raise ParseException("if needs to be followed by a condition in parentheses")
            closed_parentheses_index = find_matching_brace(tokens,  open_parentheses_index)
            condition_tokens = tokens[open_parentheses_index+1:closed_parentheses_index]

            open_curly_index = closed_parentheses_index + 1
            
            if type(tokens[open_curly_index]) is not OPEN_CURLY:
                raise ParseException()
            condition_tree = parse_expression(condition_tokens)
        elif start_type is OPEN_CURLY:
            reached_else = True
            open_curly_index = start_index
            condition_tree = NUMBER(1)

        else:
            raise ParseException()


        closed_curly_index = find_matching_brace(tokens, open_curly_index)

        
        block_tokens = tokens[open_curly_index+1:closed_curly_index]

        block_tree = parse_code(block_tokens, True)

        if_block = If_Block(condition_tree, block_tree)
        if_blocks.append(if_block)

        following_token_index = closed_curly_index + 1

        len(tokens) == following_token_index


        reached_end = \
            len(tokens) == following_token_index or \
            type(tokens[following_token_index]) is not ELSE_KEYWORD
        
        if reached_end:
            if_container = If_Container(if_blocks)
            return [if_container, following_token_index]
        
        if reached_else:
            raise ParseException("cannot have more cases after else")
        
        next_if_token_index = following_token_index + 1

        start_index = next_if_token_index




def parse_block(tokens: list[Token], open_curly_index: int, inside_function:bool = False) -> Any:
    
    index = open_curly_index
    previous_token = tokens[index-1]
    closed_curly_index = find_matching_brace(tokens, index)
    end_block_idx = closed_curly_index+1

    assert type(previous_token) is not EQUAL, "should have been checked"

    if type(previous_token) is VARIABLE and type(tokens[index-2]) is STRUCT_KEYWORD:
        if type(tokens[closed_curly_index+1]) is not SEMICOLON:
            raise Exception("struct must end with semicolon")
        struct_contents = tokens[index+1:closed_curly_index]
        struct_fields = []
        variable_tokens: list[Token] = []
        for struct_token in struct_contents:
            if type(struct_token) is SEMICOLON:
                struct_fields.append(get_typed_variable(variable_tokens))
                variable_tokens = []
            else:
                variable_tokens.append(struct_token)
        if len(variable_tokens) != 0: raise Exception()
        new_struct = Struct(previous_token.name, len(struct_fields), struct_fields)
        start_block_idx = open_curly_index - 2
        # +1 cause of the semicolon
        return [new_struct, start_block_idx, end_block_idx+1]

    if type(previous_token) is not CLOSED_PAREN:
        raise ParseException("invalid token before open curly")
    
    open_paren_index = find_matching_brace(tokens, index-1)

    keyword_index = open_paren_index - 1

    keyword = tokens[keyword_index]
    keyword_type = type(keyword)

    paren_tokens = tokens[open_paren_index+1:open_curly_index-1]
    curly_tokens = tokens[open_curly_index+1:closed_curly_index]

    statement_count = 0
    statement_tokens = []

    is_function = keyword_type is VARIABLE
    if is_function and inside_function:
        raise ParseException("cannot have nested functions")
    new_inside_function = is_function or inside_function
    block = parse_code(curly_tokens, new_inside_function)

    start_block_idx = open_paren_index - 1

    new_block: Block

    if keyword_type is FOR_KEYWORD:

        if type(paren_tokens[-1]) is SEMICOLON:
            raise ParseException("for loop incrementer must not end in a semicolon")

        paren_tokens.append(SEMICOLON())
        for token in paren_tokens:
            if type(token) is not SEMICOLON:
                statement_tokens.append(token)
                continue
            if statement_count == 0:
                initializer = parse_line(statement_tokens)
            elif statement_count == 1:
                condition = parse_line(statement_tokens)
            elif statement_count == 2:
                incrementer = parse_line(statement_tokens)
            else:
                raise ParseException("more than three statements in the for loop parentheses")
            statement_count += 1
            statement_tokens = []
            
        if statement_count < 3:
            raise ParseException("less than three statements in the for loop parentheses")

        
        if type(initializer) is not Assignment:
            raise ParseException("initializer must be an assignment")
        if type(condition) is not Operation:
            raise ParseException("condition must be an operation")        
        if type(incrementer) is not Assignment:
            raise ParseException("incrementer must be an assignment")        
        new_block = For_Block(initializer, condition, incrementer, block)

    elif keyword_type is WHILE_KEYWORD:

        condition = parse_expression(paren_tokens)

        new_block = While_Block(condition, block)

    elif keyword_type is IF_KEYWORD:

        [if_container, next_token_index] = parse_if_else_blocks(tokens, keyword_index )

        return [if_container, start_block_idx, next_token_index]
        
    elif keyword_type is VARIABLE:
        # must be a function
        # get output type
        previous_block_index = open_paren_index
        while True:
            if type(tokens[previous_block_index]) in [SEMICOLON, CLOSED_CURLY]: break
            if previous_block_index == -1: break
            previous_block_index -= 1
        type_tokens = tokens[previous_block_index+1:open_paren_index-1]
        output_type = get_type(type_tokens)
        parameters = parse_function_parameters(paren_tokens)
        new_block = Function_Block(output_type, keyword.name, parameters, block)
        start_block_idx = open_paren_index-1-len(type_tokens)

    else:
        raise ParseException("must have a function name or keyword before the parentheses before curly braces")

    return [new_block, start_block_idx, end_block_idx]
    
def parse_array_literal(array_tokens: list[Token]) -> Array_Literal:

    assert type(array_tokens[0]) is OPEN_CURLY, "shouldnt have entered here"

    if type(array_tokens[-1]) is not CLOSED_CURLY:
        raise ParseException("no matching brace for array")
    
    items = []

    expression_tokens: list[Token] = []

    inside_array_tokens = array_tokens[1:-1]

    if len(inside_array_tokens) == 0:
        raise NotImplementedYetException("not supporting empty arrays, adds a wrinkle to asm generation so nahhh")

    inside_array_tokens.append(COMMA())

    for token in inside_array_tokens:

        if type(token) is COMMA:

            items.append(parse_expression(expression_tokens))
            expression_tokens = []
        else:
            expression_tokens.append(token)

        

    return Array_Literal(len(items), items)


def parse_leaf(tokens: list[Token]) -> Tree:

    tree:Tree = None

    assert len(tokens) > 0

    # REFACTOR
    # doing this in parseleaf is the most straightforward
    # but this really no longer a leaf now
    if type(tokens[0]) is NOT:
        sub_leaf = parse_expression(tokens[1:])
        return UnitaryOperation(sub_leaf, tokens[0])

    token_idx = 0

    
    is_casted = type(tokens[0]) is OPEN_PAREN
    is_null = len(tokens) == 0 and type(tokens[0]) is NULL_KEYWORD


    if is_casted:
        closing_cast_idx = find_matching_brace(tokens, 0)

        casted_type_tokens = tokens[1:closing_cast_idx]

        casted_type = get_type(casted_type_tokens)

        casted_node_tokens = tokens[closing_cast_idx+1:]

        casted_node = parse_expression(casted_node_tokens)

        return Type_Cast(casted_node, casted_type)
    elif is_null:

        return tokens[0]


    while True:
        
        if token_idx == len(tokens): break

        token = tokens[token_idx]


        if type(token) is REFERENCE:
            if token_idx != 0: raise ParseException()
            if len(tokens) != 2: raise ParseException()
            variable_token = tokens[token_idx+1]
            if type(variable_token) is not VARIABLE:
                raise ParseException()
            tree = Reference(variable_token.name)
            next_token_idx = token_idx + 2
        elif type(token) in [DOT, FIELD_REFERENCE]:
            if token_idx == 0: raise ParseException()
            if token_idx == len(tokens)-1: raise ParseException()
            next_token = tokens[token_idx+1]
            # if type(prev_token) is not VARIABLE: raise ParseException()
            if type(next_token) is not VARIABLE: raise ParseException()
            assert tree is not None
            if type(token) is DOT:
                tree = Struct_Field(tree, next_token.name)
            elif type(token) is FIELD_REFERENCE:
                tree = Struct_Field(Array_Index(tree, NUMBER(0)), next_token.name)
            else: assert False
            next_token_idx = token_idx+2
            
        elif type(token) is OPEN_BRACKET:

            if token_idx == 0: raise ParseException()
            assert tree is not None

            closed_bracket_idx = find_matching_brace(tokens, token_idx)

            # if closed_bracket_idx+1 != len(tokens): raise ParseException()

            index_tokens = tokens[token_idx+1:closed_bracket_idx]

            index_tree = parse_expression(index_tokens)

            tree = Array_Index(tree, index_tree)

            next_token_idx = closed_bracket_idx+1

        elif type(token) is OPEN_PAREN:

            if token_idx == 0: raise ParseException()
            assert tree is not None

            closed_parentheses_idx = find_matching_brace(tokens, token_idx)

            argument_tokens = tokens[token_idx+1:closed_parentheses_idx]

            argument_tree = parse_function_arguments(argument_tokens)


            # note that this breaks if functions are first class
            # e.g. a[1](bop)    where a is an array of functions
            # im not doing that though

            if type(tree) is not VARIABLE: raise ParseException()

            tree = Function_Call(tree.name, argument_tree)


            next_token_idx = closed_parentheses_idx+1



        elif type(token) in [NULL_KEYWORD,VARIABLE, NUMBER, CHAR, STRING]:

            tree = token
            next_token_idx = token_idx+1

        elif type(token) is CLOSED_BRACKET:
            raise ParseException()
        else:
            raise ParseException("invalid token: ",token)



        token_idx = next_token_idx


    assert tree is not None
    return tree






def parse_expression(expression_tokens: list[Token]) -> Tree:

    if len(expression_tokens) == 0:
        raise ParseException("could mean nothing after the equal sign, or two semicolons next to eachother")

    weights = [token.order_weight for token in OP_TOKENS]
    min_weight = min(weights)
    max_weight = max(weights)

    def parse_sub_expression(expression: list[Token], weight:int = min_weight) -> Tree:

        depth = 0
        matching_operations = [operation for operation in OP_TOKENS if operation.order_weight == weight]
        branch_start_idx = 0
        previous_operation = None
        tree: Tree = None

        if type(expression[-1]) in OP_TOKENS:
            raise ParseException("expression ends in operation")

        # this is just so it's able to pick up the final subexpression
        dummy_operation = matching_operations[0]
        expression = expression.copy()
        expression.append(dummy_operation())



        for (token_idx, token) in enumerate(expression):

            if type(token) is EQUAL:
                raise ParseException("expression cannot have an equal sign")
            
            if type(token) is SEMICOLON:
                raise ParseException("expression cannot have a semicolon")
            

            if type(token) in [OPEN_PAREN, OPEN_BRACKET]: depth += 1
            if type(token) in [CLOSED_PAREN, CLOSED_BRACKET]: depth -= 1

            if depth > 0: continue

            ## FUTURE this might break for expressions starting with a negative sign
            # right now i'm only supporting unsigned ints though so ok
            if type(token) not in matching_operations: continue    
            
            sub_expression = expression[branch_start_idx:token_idx]


            if len(sub_expression) == 0:
                if branch_start_idx == 0:
                    raise ParseException("expression cannot start with an operation (no negatives for now)")
                else:
                    raise ParseException("multiple operations in a row")

            previous_token_type = type(expression[token_idx-1])
            if previous_token_type is CLOSED_PAREN:
                open_paren_idx = find_matching_brace(expression, token_idx-1)
                is_arithmetic_parentheses_group = open_paren_idx == branch_start_idx            
            else:
                is_arithmetic_parentheses_group = False
            
            at_leaf = weight == max_weight
                
            if is_arithmetic_parentheses_group:
                new_branch = parse_sub_expression(sub_expression[1:-1], min_weight)
            elif at_leaf:
                # new_branch = parse_expression_leaf(sub_expression)
                new_branch = parse_leaf(sub_expression)
            else:
                new_branch = parse_sub_expression(sub_expression, weight+1)

            branch_start_idx = token_idx + 1

            if tree is None:
                tree = new_branch
            else:
                tree = Operation(tree, previous_operation, new_branch)
            
            previous_operation = token

        if depth != 0: 
            raise ParseException(f"mismatched parentheses in expression: {expression_tokens}")

        return tree

    expression_tree = parse_sub_expression(expression_tokens)
    return expression_tree



def parse_function_parameters(parameter_tokens: list[Token]) -> list[Tree]:

    parameters: list[Tree] = []

    if len(parameter_tokens) == 0:
        return []

    if type(parameter_tokens[-1]) is COMMA:
        raise ParseException("cannot end parameter list with a comma just cause im mean like that (:<")

    parameter_tokens.append(COMMA())

    variable_tokens: list[Token] = []

    for token in parameter_tokens:

        if type(token) is COMMA:
            parameters.append(get_typed_variable(variable_tokens))
            variable_tokens = []
        else:
            variable_tokens.append(token)

    return parameters

def parse_function_arguments(argument_tokens: list[Token]) -> list[Tree]:
    
    arguments: list[Tree] = []
    start_argument_idx = 0

    if len(argument_tokens) == 0:
        return arguments

    if type(argument_tokens[-1]) is COMMA:
        raise ParseException("cant end arguments in a comma")
    
    argument_tokens.append(COMMA())

    depth = 0

    for idx, token in enumerate(argument_tokens):

        if type(token) in open_tokens:
            depth += 1
        elif type(token) in closed_tokens:
            depth -= 1

        if depth > 0: continue
        if depth < 0: raise ParseException("mismatched parentheses")

        if type(token) is COMMA:
            if idx == start_argument_idx:
                raise ParseException("multiple commas in a row (or starts with a comma)")
            argument_tree = parse_expression(argument_tokens[start_argument_idx:idx])
            arguments.append(argument_tree)
            start_argument_idx = idx+1
        
    return arguments

def parse_line(line_tokens: list[Token]) -> Tree:

    equal_sign_found = False
    return_found = False
    is_continue = False
    is_break = False

    equal_idx:int = None
    for idx in range(len(line_tokens)):
        token = line_tokens[idx]
        if type(token) in ASSIGNMENT_TOKENS:
            if equal_sign_found:
                raise ParseException("only one equal in line")
            equal_idx = idx
            equal_sign_found = True        
        elif type(token) is RETURN_KEYWORD:
            if return_found:
                raise ParseException("only one return in line")
            if idx != 0:
                raise ParseException("line must start with return")
            return_found = True
        elif type(token) is CONTINUE_KEYWORD:
            
            if len(line_tokens) != 1: raise ParseException("continue must be on its own line")
            is_continue = True
        elif type(token) is BREAK_KEYWORD:
            
            if len(line_tokens) != 1: raise ParseException("break must be on its own line")
            is_break = True
            



    if equal_sign_found and return_found:
        raise ParseException("cant have an assignment and return on the same line")
    


    if equal_sign_found:

        assignment_token = line_tokens[equal_idx]

        lhs_tokens = line_tokens[0:equal_idx]
        if len(lhs_tokens) == 0:
            raise ParseException("need something before the equal sign")
        

        rhs_tokens = line_tokens[equal_idx+1:]

        is_typed = type(lhs_tokens[0]) in [Base_Types, STRUCT_KEYWORD]

        is_array_literal = type(rhs_tokens[0]) is OPEN_CURLY

        if is_array_literal and not is_typed:
            raise Exception("can only have an array literal for a declaration")
        
        rhs: Tree
        if is_array_literal:
            rhs = parse_array_literal(rhs_tokens)
        else:
            rhs = parse_expression(rhs_tokens)


        target: Tree
        if is_typed:
            if type(assignment_token) is not EQUAL:
                raise ParseException(f"declaration cannot have {type(assignment_token)}")
            if is_array_literal:
                ## FUTURE brackets can enclose number of elemeents
                type_tokens = lhs_tokens[0:-2]
                [open_bracket, close_bracket] = lhs_tokens[-2:]
                if type(open_bracket) is not OPEN_BRACKET or type(close_bracket) is not CLOSED_BRACKET:
                    raise ParseException()
                target = get_typed_variable(type_tokens)
                target.type.reference_level += 1
            else:
                target = get_typed_variable(lhs_tokens)

            return Declaration(target, rhs)

        else:
            target = parse_leaf(lhs_tokens)

            if type(target) is Function_Call:
                raise ParseException("cannot assign to a function call")
            
            if type(assignment_token) is PLUS_EQUAL:
                return Assignment(target, Operation(target, PLUS(), rhs))
            elif type(assignment_token) is MINUS_EQUAL:
                return Assignment(target, Operation(target, MINUS(), rhs))
            elif type(assignment_token) is TIMES_EQUAL:
                return Assignment(target, Operation(target, ASTERISK(), rhs))
            elif type(assignment_token) is EQUAL:
                return Assignment(target, rhs)
            else: assert False

    elif return_found:

        assert type(line_tokens[0]) is RETURN_KEYWORD
        if len(line_tokens) == 1:
            return_value = None
        else:
            return_value = parse_expression(line_tokens[1:])
        return Return(value = return_value)
    elif is_continue or is_break:
        return line_tokens[0]
    elif type(line_tokens[0]) in [Base_Types, STRUCT_KEYWORD]:
        # uninitialized declaration
        return Declaration(get_typed_variable(line_tokens), None)
    else:
        return parse_expression(line_tokens)
            

def group_into_lines(tokens: list[Token]) -> list[Tree]:

    if tokens == []: return []

    lines = []
    line_tokens:list[Token] = []

    for token in tokens:
        if type(token) is SEMICOLON:
            if len(line_tokens) == 0: raise ParseException("empty line (semicolon without something before it)")
            lines.append(parse_line(line_tokens))
            line_tokens = []
        else:
            line_tokens.append(token)
    
    if type(tokens[-1]) is not SEMICOLON:
        raise ParseException("last line in the block didn't end with semicolon")

    return lines



def parse_code(tokens: list[Token], inside_function:bool = False) -> Tree:
    partial_syntax_tree = []
    open_curly_indices = []
    depth = 0
    previous_end_index = 0
    i = 0

    while i < len(tokens):



        token = tokens[i]

        token_type = type(token)
        previous_token_type = type(tokens[i-1])
        is_block_start = token_type is OPEN_CURLY and depth == 0 and previous_token_type is not EQUAL




        if is_block_start:
            open_curly_indices.append(i)
            [block, start_index, end_index] = parse_block(tokens, i, inside_function)

            partial_syntax_tree += group_into_lines(tokens[previous_end_index:start_index])
            partial_syntax_tree.append(block)

            previous_end_index = end_index
            i = end_index
        else:
            i+=1

            if token_type in open_tokens:
                depth += 1
            elif token_type in closed_tokens:
                depth -= 1

    partial_syntax_tree += group_into_lines(tokens[previous_end_index:])


    for item in partial_syntax_tree:
        if not inside_function and type(item) not in [Declaration, Struct, Function_Block]:
            raise ParseException("global scope can only contain declarations, structs, and functions")

    return partial_syntax_tree
    


TEMP_REG = "r29"
RIGHT_TEMP_REG = "r30"

jump_count = [0]
functions_reached: list[Function_Block] = []


@dataclass
class Variable_Allocated:
    name: str
    type: Type
    base_pointer_offset: int
    size: int


# variables and structs should probably also be global
GLOBALS: list[Variable_Allocated] = []

def flatten(nested: list[list[Any]]) -> list[Any]:

    """
    flattens a list of lists
    used for flatten scoped variables or structs 
    """

    flattened = []
    for item in nested: flattened += item
    return flattened


def get_size_match_assembly(target_type: Type, source_type: Type, structs: list[list[Struct]]) -> list[str]:

    """
    
    """

    # generally only for converting to different sized integers
    # BUT for type casting, could convert between any type

    target_size = get_size(target_type, structs)
    source_size = get_size(source_type, structs)

    if target_size > source_size:
        difference = target_size - source_size
        fill_assembly = [load_immediate(0)]
        # fill_assembly = [f"ldi {TEMP_REG}, 0"]
        fill_assembly += [push()] * difference
        # fill_assembly += [f"push {TEMP_REG}"] * difference
        return fill_assembly
    else:
        difference = source_size - target_size
        return [pop()] * difference
        # return [f"pop {TEMP_REG}"] * difference




def types_match(type1: Type, type2: Type) -> bool:
    
    assert type(type1) is Type
    assert type(type2) is Type
    if type1.reference_level != type2.reference_level:
        return False
    if type(type1.base_type) is Struct_Type and type(type2.base_type) is Struct_Type:
        return type1.base_type.name == type2.base_type.name
    elif type1.reference_level == 0:

        # for now everything else is just integer types of different sizes, so it's fine
        return True
    else:
        return type1.base_type == type2.base_type

def is_int_type(node: Operation, variables: list[list[Variable_Allocated]], structs: list[list[Struct]]) -> bool:

    """
    alternatively i could do this check in each operation function
    """

    [_,node_type] = get_expression_assembly(node, variables, structs)
    
    assert type(node_type) is Type
    if node_type.reference_level != 0: return False

    return node_type.base_type in [Base_Types.INT8, Base_Types.INT16]

def get_int_type(size: int) -> Type:
    # having its own function just so i remember the size of the int types is also being defined here
    if size == 1:
        return Type(Base_Types.INT8, 0)
    else:
        return Type(Base_Types.INT16, 0)

def get_size(variable_type: Type, structs: list[list[Struct]]) -> int:
    
    is_struct = type(variable_type.base_type) is Struct_Type and variable_type.reference_level == 0
    if is_struct:
        sized_struct = get_struct(variable_type.base_type.name, structs)
        all_field_sizes = [get_size(field.type, structs) for field in sized_struct.fields]
        total_size = sum(all_field_sizes)
        return total_size
    elif variable_type.reference_level > 0:
        # pointers will be 2 bytes
        return 2
    elif variable_type.base_type is Base_Types.INT8:
        return 1
    elif variable_type.base_type is Base_Types.INT16:
        return 2
    else:
        assert False
    
def allocate_to_stack(size: int, variable_name: str|None, variable_type: Type, variables: list[list[Variable_Allocated]],  parameter_offset:int|None=None) -> None:

    """
    keeps track of where to load/store variables
    also used for array literals and strings so the data isn't overwritten (name and type are None)
    """

    is_global = len(variables) == 0

    

    if not is_global and parameter_offset is None:
        innermost_scope_space = scope_spaces[-1]
        innermost_scope_space.space += size
    

    if is_global:
        current_scope_variables = GLOBALS
        all_previous_variables = GLOBALS
    else:
        current_scope_variables = variables[-1]
        all_previous_variables = flatten(variables)

    

    if parameter_offset is not None:
        assert parameter_offset > 0
        offset_from_base_pointer = -parameter_offset
        for test in all_previous_variables:
            assert test.base_pointer_offset < 0

    elif len(all_previous_variables) == 0 or all_previous_variables[-1].base_pointer_offset < 0:
        offset_from_base_pointer = size - 1
        for test in all_previous_variables:
            assert test.base_pointer_offset < 0
    else:
        last_variable = all_previous_variables[-1]
        #FLIPPED should add the current variable size
        # offset_from_base_pointer = last_variable.base_pointer_offset + last_variable.size
        offset_from_base_pointer = last_variable.base_pointer_offset + size

    current_scope_variables.append(Variable_Allocated(variable_name, variable_type, offset_from_base_pointer, size))


def allocate_variable_to_stack(variable: Variable_Typed, variables: list[list[Variable_Allocated]], structs: list[list[Struct]], parameter_offset:int|None) -> None:

    """
    keeps track of where to load/store variables
    done for declarations and function parameters
    """

    is_global = len(variables) == 0

    if is_global:
        current_scope_variables = GLOBALS
    else:
        current_scope_variables = variables[-1]

    current_scope_variable_names = [variable.name for variable in current_scope_variables if variable.type.base_type not in PLACEHOLDER_TYPES]
    if variable.name in current_scope_variable_names:
        raise RepeatedDeclarationException(f"variable '{variable.name}' already declared")

    size = get_size(variable.type, structs)
    allocate_to_stack(size, variable.name, variable.type, variables, parameter_offset)
    

def save_struct_in_scope(struct: Struct, structs: list[list[Struct]]) -> None:

    """
    keeps track of the structs defined in the current scope
    the structs are then used when checking the type
    """

    current_scope_structs = structs[-1]
    current_scope_struct_names = [struct.name for struct in current_scope_structs]
    if struct.name in current_scope_struct_names:
        raise RepeatedDeclarationException(f"struct '{struct.name}' already declared")
    current_scope_structs.append(struct)



def get_variable(variable_name: str, variables: list[list[Variable_Allocated]]) -> Variable_Allocated:

    """
    looks through the allocated variables to find the variable by its name
    """

    is_global = len(variables) == 0

    if is_global:
        all_variables = GLOBALS
    else:
        all_variables = flatten(variables)
        all_variables.reverse()   # start with innermost scope and work outwards
        all_variables += GLOBALS
        
    for variable in all_variables:

        assert type(variable) is Variable_Allocated
        if variable.type.base_type in PLACEHOLDER_TYPES:
            continue
        if variable_name != variable.name:
            continue

        return variable

    raise UndefinedException(f"{variable_name} hasnt been defined")



def get_struct(struct_name: str, structs: list[list[Struct]]) -> Struct:
    
    """
    gets the struct, with the information on the fields, from the name
    used for getting the total size, and the location of a field
    """
    
    structs_flattened = flatten(structs)
    structs_flattened.reverse() # start with innermost scope and work outwards
    for struct in structs_flattened:
        assert type(struct) is Struct
        if struct.name == struct_name:
            return struct
    raise StructException(f"{struct_name} is not a struct")




def get_function_output_type(function_name: str) -> Type:
    
    """
    used to determine the output type of a function call
    also used for struct fields to know which part to store to TOS 
    """

    global syntax_tree
    for global_item in syntax_tree:
        if type(global_item) is not Function_Block: continue
        if global_item.name != function_name: continue
        return global_item.output_type
    raise UndefinedException(f"{function_name} is not defined")


def get_function_parameters(function_name: str) -> list[Variable_Typed]:
    
    """
    used to get the parameters of a function call
    """

    global syntax_tree
    for global_item in syntax_tree:
        if type(global_item) is not Function_Block: continue
        if global_item.name != function_name: continue
        return global_item.parameters
    raise UndefinedException(f"{function_name} is not defined")




def get_jump_point(jump_type: str) -> str:
    jump_text = f"{jump_type}_{jump_count[0]}"
    jump_count[0] += 1
    return jump_text



"""
both immediate and memory:
    store
    add
    subtract

call and return

set main
    avr: .global main
    6502: include code that sets the reset address

also for 6502, intialize the stack pointer

    

indirect load and store

for the ones that are the same (e.g. brne) i still need it indented for the 6502
    i could just have something at the end that indents all lines that don't contain a colon

    

multiply

"""


class Target(Enum):
    _6502 = auto()
    AVR = auto()


TARGET = Target._6502



def load_immediate(value: int) -> str:
    return {
        Target.AVR: f"ldi {TEMP_REG}, {value}",
        Target._6502: f"lda #{value}"
    }[TARGET]


def load_immediate_right_side_zero() -> list[str]:
    if TARGET == Target.AVR:
        return [f"ldi {RIGHT_TEMP_REG}, 0"]
    else:
        return [
            "; load rhs with 0 for higher bytes",
            f"lda #0",
            f"sta {RIGHT_SIDE_6502}"
        ]


def load_from_memory(address: int) -> str:
    return {
        Target.AVR: f"lds {TEMP_REG}, {address}",
        Target._6502: f"lda {address}"
    }[TARGET]

def store_to_memory(address: int) -> str:
    return {
        Target.AVR: f"sts {address}, {TEMP_REG}",
        Target._6502: f"sta {address}"
    }[TARGET]


def set_stack_pointer_from_memory(address_low, address_high) -> list[str]:
    """
    value in memory sent to stack pointer 
    sp = mem
    """
    match TARGET:
        case Target.AVR:
            return [
                f"lds {TEMP_REG}, {address_low}",
                f"sts {SP_ADDRESS_LOW}, {TEMP_REG}",
                f"lds {TEMP_REG}, {address_high}",
                f"sts {SP_ADDRESS_HIGH}, {TEMP_REG}"
            ]
        
        case Target._6502:
            return [
                f"ldx {address_low}",
                f"txs"
            ]
        case _: assert False

# FAST
def set_stack_pointer_from_memory_with_offset(address_low, address_high, negative_offset) -> list[str]:
    """
    value in memory sent to stack pointer 
    sp = mem
    """
    match TARGET:
        case Target.AVR:
            return [
                f"lds {TEMP_REG}, {address_low}",
                f"subi {TEMP_REG}, {negative_offset}",
                f"sts {SP_ADDRESS_LOW}, {TEMP_REG}",
                f"lds {TEMP_REG}, {address_high}",
                f"sbci {TEMP_REG}, 0",
                f"sts {SP_ADDRESS_HIGH}, {TEMP_REG}"
            ]
        
        case Target._6502:
            return [
                f"sec",
                f"lda {address_low}",
                f"sbc #{negative_offset}",
                f"tax",
                f"txs"
            ]
        case _: assert False

# FAST
def set_memory_from_stack_pointer(address_low, address_high) -> list[str]:

    """
    used for strings and arrays
    pushes the address of the last element on the stack
    since the sp points to the next slot, you add one
    mem=sp
    """

    match TARGET:
        case Target.AVR:
            return [
                f"lds {TEMP_REG}, {SP_ADDRESS_LOW}",
                f"sts {address_low}, {TEMP_REG}",
                f"lds {TEMP_REG}, {SP_ADDRESS_HIGH}",
                f"sts {address_high}, {TEMP_REG}",
            ]
        case Target._6502:
            # for 6502 the stack pointer is only one byte
            # (the high byte is always 1)
            return [
                "tsx",
                f"stx {address_low}",
                f"lda #1",
                f"sta {address_high}"
            ]
        case _: assert False


# FAST
def prepare_indirect_from_memory_with_offset(negative_offset: int, is_global) -> list[str]:
    
    """
    used for assigning a value to a variable
    stored at some location offset from the base pointer
    basse pointer is the address low and high

    negative offset is kind of ugly to have as a parameter
    for 6502 only positive offset allowed, so im lumping negative offset in here

    alternative would be subtracting after but then i would have to do this
    then load back to the accumulator
    then subtract
    then store it back

    for avr it's not an issue cause im using the x registers, which i can subtract from directly
    """

    if is_global:
        low_indirect = LOW_INDIRECT_6502_GP
        high_indirect = HIGH_INDIRECT_6502_GP
        address_low = GLOBAL_P_LOW
        address_high = GLOBAL_P_HIGH
    else:
        low_indirect = LOW_INDIRECT_6502_BP
        high_indirect = HIGH_INDIRECT_6502_BP
        address_low = BP_LOW
        address_high = BP_HIGH

    if TARGET == Target.AVR:
        return [
            f"lds {X_LOW}, {address_low}",
            f"lds {X_HIGH}, {address_high}",
            f"subi {X_LOW}, {negative_offset}",
            f"sbci {X_HIGH}, 0",
        ]
    else:
        return [
            "; prepare indirect memory offset:",
            "sec",
            f"lda {address_low}",
            f"sbc #{negative_offset}",
            f"sta {low_indirect}",
            f"lda {address_high}",
            f"sbc #{0}",
            f"sta {high_indirect}",
        ]



# FAST
def prepare_indirect_from_stack_pointer() -> list[str]:
    if TARGET == Target.AVR:
        return [
            f"lds {X_LOW}, {SP_ADDRESS_LOW}",
            f"lds {X_HIGH}, {SP_ADDRESS_HIGH}"
        ]
    else:
        
        return ["tsx"]

def load_indirect_with_offset(offset, is_global) -> list[str]:

    if is_global:
        low_indirect = LOW_INDIRECT_6502_GP
    else:
        low_indirect = LOW_INDIRECT_6502_BP
        

    if TARGET == Target.AVR:
        return [f"ldd {TEMP_REG}, X+{offset}"]
    else:
        if offset < 0: raise Exception("not sure how to do negative offset for 6502")
        assert offset < 256
        return [
            "; load indirect:",
            "; OFFSET_TEST",
            f"ldy #{offset}",
            f"lda ({low_indirect}),Y"
        ]



def load_indirect_with_offset_array(offset) -> list[str]:
    if TARGET == Target.AVR:
        return [f"ldd {TEMP_REG}, X+{offset}"]
    else:
        if offset < 0: raise Exception("not sure how to do negative offset for 6502")
        assert offset < 256
        return [
            "; load indirect:",
            "; OFFSET_TEST",
            f"ldy #{offset}",
            f"lda ({LOW_INDIRECT_6502_ARRAY}),Y"
        ]

def load_indirect_sp_with_offset(offset) -> list[str]:
    if TARGET == Target.AVR:
        raise Exception("not implementing, screw avr")
        return [f"ldd {TEMP_REG}, X+{offset}"]
    else:
        if offset < 0: raise Exception("not sure how to do negative offset for 6502")
        return [
            "; load from stack pointer:",
            f"lda ({0x0100 + offset}),X"
        ]



def load_indirect_sp_right_side_with_offset(offset) -> list[str]:
    """
    note that i'm no longer preserving the accumulator
    so the rhs has to be loaded
    """
    if TARGET == Target.AVR:
        raise Exception("nah")
        return [f"ldd {RIGHT_TEMP_REG}, X+{offset}"]
    else:
        if offset < 0: raise Exception("not sure how to do negative offset for 6502")
        # in this case case im trying to load using y indirect
        # then store the value
        # sadly ldx doesn't have indirect mode
        return [
            "; load right-hand side:",
            "; OFFSET_TEST",
            f"lda ({0x0100 + offset}),X",
            f"sta {RIGHT_SIDE_6502}"
        ]

def store_indirect_with_offset(offset, is_global) -> list[str]:

    if is_global:
        low_indirect = LOW_INDIRECT_6502_GP
    else:
        low_indirect = LOW_INDIRECT_6502_BP
        

    if TARGET == Target.AVR:
        return [f"std X+{offset}, {TEMP_REG}"]
    else:
        if offset < 0: raise Exception("not sure how to do negative offset for 6502")
        assert offset < 256
        return [
            "; store byte",
            "; OFFSET_TEST",
            f"ldy #{offset}",
            f"sta ({low_indirect}),Y"
        ]


def store_indirect_with_offset_bp(offset) -> list[str]:

   

    if TARGET == Target.AVR:
        return [f"std X+{offset}, {TEMP_REG}"]
    else:
        if offset < 0: raise Exception("not sure how to do negative offset for 6502")
        assert offset < 256
        return [
            "; store byte",
            "; OFFSET_TEST",
            f"ldy #{offset}",
            f"sta ({BP_LOW}),Y"
        ]



def store_indirect_with_offset_array(offset) -> list[str]:
    if TARGET == Target.AVR:
        return [f"std X+{offset}, {TEMP_REG}"]
    else:
        if offset < 0: raise Exception("not sure how to do negative offset for 6502")
        assert offset < 256
        return [
            "; store byte",
            "; OFFSET_TEST",
            f"ldy #{offset}",
            f"sta ({LOW_INDIRECT_6502_ARRAY}),Y"
        ]



def store_indirect_sp_with_offset(offset) -> list[str]:
    if TARGET == Target.AVR:
        raise Exception("nah")
        return [f"std X+{offset}, {TEMP_REG}"]
    else:
        if offset < 0: raise Exception("not sure how to do negative offset for 6502")
        return [
            "; store byte",
            "; OFFSET_TEST",
            f"sta ({0x0100 + offset}),X"
        ]

def compare_two_sides() -> str:
    return {
        Target.AVR: f"cp {TEMP_REG}, {RIGHT_TEMP_REG}",
        Target._6502: f"cmp {RIGHT_SIDE_6502}"
    }[TARGET]
    


    
def push() -> str:
    return {
        Target.AVR: f"push {TEMP_REG}",
        Target._6502: "pha"
    }[TARGET]

def pop() -> str:
    return {
        Target.AVR: f"pop {TEMP_REG}",
        Target._6502: "pla" 
    }[TARGET]
            

def compare_immediate(value: int) -> str:
    return {
        Target.AVR: f"cpi {TEMP_REG}, {value}",
        Target._6502: f"cmp #{value}"
    }[TARGET]


def compare_from_memory(address: int) -> str:
    return {
        Target.AVR: f"cp {TEMP_REG}, {address}",
        Target._6502: f"cmp {address}"
    }[TARGET]

def call_subroutine(name: str) -> str:
    return {
        Target.AVR: f"call {name}",
        Target._6502: f"jsr {name}"
    }[TARGET]

def subtract_immediate(value: int) -> list[str]:
    match TARGET:
        case Target.AVR:
            return [f"subi {TEMP_REG}, {value}"]
        case Target._6502:
            return [
                "sec",
                f"sbc #{value}"
            ]
        case _: assert False

def subtract_immediate_with_carry(value: int) -> str:
    return {
        Target.AVR: f"sbci {TEMP_REG}, {value}",
        Target._6502: f"sbc #{value}"
    }[TARGET]


def branch_to_jump_6502(branch_mnemonic: str, final_destination_label: str) -> list[str]:

    # just a hack cause you can only branch 128 bytes away
    # and i'm being super inefficient with generating machine code

    assert TARGET is Target._6502

    jump_skip_point = get_jump_point("jump_skip")
    branch_selected_point = get_jump_point("branch_selected")


    return [
        f"{branch_mnemonic} {branch_selected_point}",
        f"jmp {jump_skip_point}",
        f"{branch_selected_point}:",
        f"jmp {final_destination_label}",
        f"{jump_skip_point}:"

    ]


def branch_not_equal(label: str) -> list[str]:
    match TARGET:
        case Target.AVR:
            return [f"brne {label}"]
        case Target._6502:
            return branch_to_jump_6502("bne", label)
        
    
def branch_equal(label: str) -> list[str]:
    
    match TARGET:
        case Target.AVR:
            return [f"breq {label}"]
        case Target._6502:
            return branch_to_jump_6502("beq", label)
    



def return_from_subroutine() -> str:
    return {
        Target.AVR: f"ret",
        Target._6502: f"rts"
    }[TARGET]





def push_stack_pointer() -> list[str]:

    """
    used for strings and arrays
    pushes the address of the last element on the stack
    since the sp points to the next slot, you add one
    """

    match TARGET:
        case Target.AVR:
            return [
                "; push the address of the string pointer",
                f"lds {TEMP_REG}, {SP_ADDRESS_LOW}",
                f"lds {RIGHT_TEMP_REG}, {SP_ADDRESS_HIGH}",
                f"addi {TEMP_REG}, {1}",  # subtraction sets/clears carry flag for higher byte
                f"adci {RIGHT_TEMP_REG}, {0}",  # tempreg - carryflag - 0
                "clc",
                f"push {TEMP_REG}",
                f"push {RIGHT_TEMP_REG}",
            ]
        case Target._6502:
            # for 6502 the stack pointer is only one byte
            # (the high byte is always 1)
            return [
                "tsx",
                "txa",
                "clc",
                f"adc #{1}",        
                "pha",
                f"lda #1",
                "pha"
            ]
        case _: assert False

def get_multiply_assembly(expression:Operation, variables: list[list[Variable_Allocated]], structs: list[list[Struct]]) -> list[Any]:

    assembly = []
    operand_type = Type(Base_Types.INT8, 0)

    [assembly1, type1] = get_expression_assembly(expression.operand1, variables, structs)
    assembly += assembly1
    assembly += get_size_match_assembly(operand_type, type1, structs)

    [assembly2, type2] = get_expression_assembly(expression.operand2, variables, structs)
    assembly += assembly2
    assembly += get_size_match_assembly(operand_type, type2, structs)
    
    match TARGET:
        case Target.AVR:
        


            output_register_low = "r0"
            output_register_high = "r1"
            
            assembly += [
                f"pop {RIGHT_TEMP_REG}",
                f"pop {TEMP_REG}",
                f"mul {TEMP_REG}, {RIGHT_TEMP_REG}",
                f"mov {TEMP_REG}, {output_register_low}",
                f"push {TEMP_REG}",
                f"mov {TEMP_REG}, {output_register_high}",
                f"push {TEMP_REG}"
            ]
            

        case Target._6502:

            loop_point = get_jump_point("multiply_loop")
            assembly += [
                "pla",
                "tax",
                "pla",
                f"sta {RIGHT_SIDE_6502}",
                "lda #0",
                "clc",
                f"{loop_point}:",
                f"adc {RIGHT_SIDE_6502}",
                "dex",
                f"bne {loop_point}",
                "pha",
                "lda #0; FUTURE right now im assuming the product is only 1 byte",
                "pha"
            ]

            
        case _: assert False
        
    return [assembly, Type(Base_Types.INT16, 0)]








def get_not_assembly(expression:UnitaryOperation, variables: list[list[Variable_Allocated]], structs: list[list[Struct]]) -> list[Any]:
    
    """
    very similar to get boolean asm but it's ok
    """

    assembly: list[str] = []



    [input_assembly, input_type] = get_expression_assembly(expression.operand, variables, structs)
    assembly += input_assembly

    size = get_size(input_type, structs)

    is_true_point = get_jump_point("not_1_to_0")
    exit_point = get_jump_point("not_exit")

    for _ in range(size):
        assembly += [
            pop(),
            compare_immediate(0),
        ]
        assembly += branch_not_equal(is_true_point)

    assembly += [
        load_immediate(1),
        f"jmp {exit_point}",
        f"{is_true_point}:",
        load_immediate(0),
        f"{exit_point}:",
        push()
    ]


    return [assembly, Type(Base_Types.INT8, 0)]




def get_and_or_assembly(expression:Operation, variables: list[list[Variable_Allocated]], structs: list[list[Struct]]) -> list[Any]:

    assembly: list[str] = []

    [assembly1, type1] = get_boolean_assembly(expression.operand1, variables, structs)
    assembly += assembly1
    assert get_size(type1, structs) == 1
    
    [assembly2, type2] = get_boolean_assembly(expression.operand2, variables, structs)
    assembly += assembly2
    assert get_size(type2, structs) == 1

    if type(expression.operation) is AND:
        either_point = get_jump_point("and_clear")
        skip_point = get_jump_point("and_skip_clear")
        value_either = 0
        value_both = 1
    elif type(expression.operation) is OR:
        either_point = get_jump_point("or_set")
        skip_point = get_jump_point("or_skip_set")
        value_either = 1
        value_both = 0
    else:
        assert False

    assembly += [
        pop(),
        compare_immediate(value_either),
        *branch_equal(either_point),
        pop(),
        compare_immediate(value_either),
        *branch_equal(either_point),
        load_immediate(value_both),
        f"jmp {skip_point}",
        f"{either_point}:",
        load_immediate(value_either),
        f"{skip_point}:",
        push()
    ]

    return [assembly, Type(Base_Types.INT8, 0)]





def get_add_subtract_assembly(expression:Operation, variables: list[list[Variable_Allocated]], structs: list[list[Struct]]) -> list[Any]:
    # it looks like c just takes the first operand, but im gonna be better than c :)
    # so i dont have the same rule in two places, i could modify getoutputtype function, and then call it here and get the size instead
    
    assembly = []

    [assembly1, type1] = get_expression_assembly(expression.operand1, variables, structs)
    [assembly2, type2] = get_expression_assembly(expression.operand2, variables, structs)
    assembly += assembly1
    assembly += assembly2
    
    size1 = get_size(type1, structs)
    size2 = get_size(type2, structs)

    assert type(type1) is Type
    is_pointer_arithmetic = type1.reference_level > 0

    assert type(type2) is Type
    if type2.reference_level > 0:
        raise TypeException("only the first operand can be a pointer")
    

    
    if type(expression.operation) is PLUS:
        arithmetic_mnemonic = "adc"
    elif type(expression.operation) is MINUS:
        arithmetic_mnemonic = "sbc"
    elif type(expression.operation) is BIT_AND:
        arithmetic_mnemonic = "and"
    elif type(expression.operation) is BIT_OR:
        arithmetic_mnemonic = "ora"
    else:
        assert False

    output_size = max(size1, size2)

    assembly.append("")
    assembly.append("; perform addition/subtraction:")
    if type(expression.operation) is MINUS and TARGET is Target._6502:
        assembly.append("sec")
    else:
        assembly.append("clc")
    
    assembly += prepare_indirect_from_stack_pointer()
    for byte_idx in range(output_size):
        offset1 = size2 + size1 - byte_idx
        offset2 = size2 - byte_idx
        if byte_idx >= size1:
            load_lhs_assembly = [load_immediate(0)]
        else:
            load_lhs_assembly = load_indirect_sp_with_offset(offset1)
        if byte_idx >= size2:
            load_rhs_assembly = load_immediate_right_side_zero()
        else:
            load_rhs_assembly = load_indirect_sp_right_side_with_offset(offset2) 
        # flipped order so rhs doesn't overwrite the accumulator
        assembly += load_rhs_assembly
        assembly += load_lhs_assembly

        if TARGET == Target.AVR:
            arithmetic_instruction = f"{arithmetic_mnemonic} {TEMP_REG}, {RIGHT_TEMP_REG}"
        else:
            arithmetic_instruction = f"{arithmetic_mnemonic} {RIGHT_SIDE_6502}"
        assembly.append(arithmetic_instruction)
        assembly.append("; store output, pop so output's on top")
        assembly += store_indirect_sp_with_offset(offset1)


    output_type = get_int_type(output_size) 

    total_input_size = size1 + size2
    assembly += [pop()] * (total_input_size - output_size)
    return [assembly, output_type]
    




def get_equality_assembly(expression:Operation, variables: list[list[Variable_Allocated]], structs: list[list[Struct]]) -> list[Any]:

    assembly: list[str] = []

    [assembly1, type1] = get_expression_assembly(expression.operand1, variables, structs)
    [assembly2, type2] = get_expression_assembly(expression.operand2, variables, structs)
    assembly += assembly1
    assembly += assembly2

    assembly.append("clc")
    assembly += prepare_indirect_from_stack_pointer()
    
    size1 = get_size(type1, structs)
    size2 = get_size(type2, structs)

    n_bytes_to_check = max(size1, size2)

    not_equal_point = get_jump_point("equal_false")
    exit_point = get_jump_point("equal_exit")




    for byte_idx in range(n_bytes_to_check):

        offset1 = size2 + size1 - byte_idx
        offset2 = size2 - byte_idx
        if byte_idx >= size1:
            load1_assembly = [load_immediate(0)]
        else:
            load1_assembly = load_indirect_sp_with_offset(offset1)
        if byte_idx >= size2:
            load2_assembly = load_immediate_right_side_zero()
        else:
            load2_assembly = load_indirect_sp_right_side_with_offset(offset2)
        assembly += load2_assembly
        assembly += load1_assembly
        assembly += [
            compare_two_sides(),
        ]
        assembly += branch_not_equal(not_equal_point)




    total_offset = size1 + size2
    new_size = 1

    if type(expression.operation) is EQUAL_COMPARE:
        is_equal_output_value = 1
        not_equal_output_value = 0
    elif type(expression.operation) is NOT_EQUAL:
        is_equal_output_value = 0
        not_equal_output_value = 1

    assembly += [
        load_immediate(is_equal_output_value),
        f"jmp {exit_point}",
        f"{not_equal_point}:",
        load_immediate(not_equal_output_value),
        f"{exit_point}:",
    ]
    assembly += store_indirect_sp_with_offset(total_offset)

    assembly += [pop()] * (total_offset - new_size)



    return [assembly, Type(Base_Types.INT8,0)]
    
    


def get_inequality_assembly(expression:Operation, variables: list[list[Variable_Allocated]], structs: list[list[Struct]]) -> list[Any]:
    
    """
    a > b
    turns into 
    b - a

    then check the carry flag

    for avr

    a>b -->
    b-a<0 -->
    carry flag set -->
    true

    
    for 6502 the carry flag is flipped
    """

    assembly: list[str] = []

    skip_clear_point = get_jump_point("greater_true")


    if type(expression.operation) in [GREATER_THAN, LESS_THAN]:
        
        carry_check_instruction = {
            Target.AVR: [f"brcs {skip_clear_point}"],
            Target._6502: branch_to_jump_6502("bcc", skip_clear_point)
        }[TARGET]
    elif type(expression.operation) in [GREATER_EQUAL, LESS_EQUAL]:
        carry_check_instruction = {
            Target.AVR: [f"brcc {skip_clear_point}"],
            Target._6502: branch_to_jump_6502("bcs", skip_clear_point)
        }[TARGET]
    else:
        assert False

    if type(expression.operation) in [GREATER_THAN, LESS_EQUAL]:
        subtraction_tree = Operation(expression.operand2, MINUS(), expression.operand1)
    elif type(expression.operation) in [LESS_THAN, GREATER_EQUAL]:
        subtraction_tree = Operation(expression.operand1, MINUS(), expression.operand2)
    else: 
        assert False

    [subtract_assembly, output_type] = get_add_subtract_assembly(subtraction_tree, variables, structs)
    
    output_size = get_size(output_type, structs)
    
    assembly += subtract_assembly
    assembly += [pop()] * output_size


    assembly += [
        load_immediate(1),
        *carry_check_instruction,
        # f"{carry_check_instruction} {skip_clear_point}",
        load_immediate(0),
        f"{skip_clear_point}:",
        push(),
    ]

    return [assembly, Type(Base_Types.INT8, 0)]








def get_string_assembly(string: STRING, variables: list[list[Variable_Allocated]], structs: list[list[Struct]]) -> list[str]:

    """
    """


    n_chars = len(string.value)

    # each char is one byte
    # plus one for null at the end
    string_size = n_chars + 1
    string_assembly = [
        "",
        "; generating string assembly",
        load_immediate(0),
        push()
    ]
    reversed_string_chars = string.value[::-1]
    for char in reversed_string_chars:
        string_assembly += [
            load_immediate(ord(char)),
            push()
        ]

    string_assembly += push_stack_pointer()
        
    allocate_to_stack(string_size, None, Type(Base_Types.STRING_PLACEHOLDER, 0), variables)


    

    return string_assembly





def get_array_assembly(target: Variable_Typed, array_literal: Array_Literal, variables: list[list[Variable_Allocated]], structs: list[list[Struct]]) -> list[Any]:

    """
    for an array literal so only called for declarations
    declaration starts by adding the variable to stack, which in turn allocates to stack
    this function does the actual pushes for that allocation
    it then allocates space for all the elements, and adds asm pushes each one
    """



    item_type_from_declaration = Type(target.type.base_type, target.type.reference_level-1)

    
    assert type(array_literal) is Array_Literal

    item_size = get_size(item_type_from_declaration, structs)
    array_size = array_literal.n_items * item_size


    array_assembly = []

    allocate_to_stack(array_size, target.name, Type(Base_Types.ARRAY_PLACEHOLDER, 0), variables)

    reversed_items = array_literal.items.copy()
    reversed_items.reverse()

    for _, item in enumerate(reversed_items):
        [item_assembly, item_type] = get_expression_assembly(item, variables, structs)
        if not types_match(item_type_from_declaration, item_type):
            raise TypeException("array types need to be all the same")
        array_assembly += item_assembly
        array_assembly += get_size_match_assembly(item_type_from_declaration, item_type, structs)



    array_assembly += push_stack_pointer()

    assert type(item_type) is Type
    array_type = Type(item_type.base_type, item_type.reference_level+1)

    return [array_assembly, array_type]



# FAST
def store_to_stack(offset_from_base_pointer: int, variable_size: int, is_global: bool) -> list[str]:
    
    """
    stores a value assigned to a variable to the proper location in the stack
    assumes the value is at TOS
    """
    


    """
    for the 6502 you can only do positive offset
    so i firt subtract the offset from X
    then add back the byte offset
    """
    assembly = []
    # if not is_global:
    #     assembly += prepare_indirect_from_memory_with_offset(OFFSET_TEST, is_global)


    #FLIPPED go from 0 to n
    # for byte_idx in range(variable_size-1,-1,-1):
    for byte_idx in range(variable_size):
        assembly += [
            pop(), 
            # of course this is fine for avr, but to keep it consistent not gonna do it this way
            # equivalent to what im doing now
                # first subtract the offset from X
                # then do a positive offset store by the byte idx
            # f"std X-{offset_from_base_pointer-byte_idx}, {TEMP_REG}"
        ]
        assembly += store_indirect_with_offset(byte_idx+OFFSET_TEST-offset_from_base_pointer, is_global)
    return assembly

# FAST
def load_from_stack(offset_from_base_pointer: int, variable_size: int, is_global: bool) -> list[str]:

    """
    retrieves a variable from inside the stack and pushes it to the top
    """

    assembly = [
        "",
        "; retrieve variable:"
    ]
    # if not is_global:
    #     assembly += prepare_indirect_from_memory_with_offset(OFFSET_TEST, is_global)

    #FLIPPED go from n to -1
    for byte_idx in range(variable_size-1,-1,-1):
        assembly += load_indirect_with_offset(byte_idx+OFFSET_TEST-offset_from_base_pointer, is_global)
        assembly += [
            "; push variable on stack:",

            #FLIPPED still subtract the offset from base pointer but add back the byteidx
            # f"ldd {TEMP_REG}, X-{offset_from_base_pointer+byte_idx}",
            
            # f"ldd {TEMP_REG}, X+{byte_idx}",
            push()
            # f"push {TEMP_REG}"
        ]
    return assembly



def get_variable_assembly(leaf: VARIABLE, is_target: bool, struct_offset: int, struct_field_size: int, variables: list[list[Variable_Allocated]], structs: list[list[Struct]]) -> list[Any]:

    """
    loads or stores a variable from/to the stack depending on istarget
    structoffset and structfieldsize allow you load/store just part of the variable
        (if the variable is struct and you just want one field of it)
    """

    assembly = []
    
    assert type(leaf) is VARIABLE


    variable = get_variable(leaf.name, variables)
    is_global = variable in GLOBALS
    
    output_type: Type = variable.type
    #FLIPPED subtract the struct offset
    # total_offset = variable.base_pointer_offset + struct_offset
    total_offset = variable.base_pointer_offset - struct_offset
    
    if struct_field_size == None:
        variable_size = get_size(output_type, structs)
    else:
        variable_size = struct_field_size

    if is_target:
        assembly += store_to_stack(total_offset, variable_size, is_global)
    else:
        assembly += load_from_stack(total_offset, variable_size, is_global)

    return [assembly, output_type]
    

def get_struct_field_assembly(leaf: Struct_Field, is_target: bool, variables: list[list[Variable_Allocated]], structs: list[list[Struct]]) -> list[Any]:

    """
    gets the assembly for something followed by some amount of field accesses (a.b.c, a().b.c, a[1].b.c)
    for just variables and for dereferences (e.g. array index) it modifies the load/store to just get the part with the field
    for function returns, it retrieves just the part for that field from the top of stack
    REFACTOR this code is very messy
    """

    struct_field = leaf
    field_names = []

    # gets the names of a series of fields  (a.b.c -> ['b','c'])
    while type(struct_field) is Struct_Field:
        field_names.append(struct_field.field_name)
        struct_field = struct_field.struct_node    
    field_names.reverse()
    inner_node = struct_field # for a.b.c the inner node would be a

    """
    this is a real mess
    to get the assembly for an array i need the offset
    the get the offset i need the struct type
    but to get the struct type i need to call the func to get the assembly
    so im gonna do it once JUST to get the type
    then the next time to get the assembly
    """
    [_, struct_type] = get_leaf_assembly(inner_node, is_target, 0, None, variables, structs)
    assert type(struct_type) is Type

    # get the total offset from the series of fields
    # gets the type of the final field
    total_field_offset = 0
    for field_name in field_names:
        is_struct = type(struct_type.base_type) is Struct_Type and struct_type.reference_level == 0
        if not is_struct:
            raise StructException("can only get a field from a stuct")
        referenced_struct = get_struct(struct_type.base_type.name, structs)
        referenced_field_names = [field.name for field in referenced_struct.fields]
        if field_name not in referenced_field_names:
            raise StructException(f"{field_name} is not a field of struct {referenced_struct}")
        field_idx = referenced_field_names.index(field_name)
        past_sizes = [get_size(field.type, structs) for field in referenced_struct.fields[0:field_idx]]
        field_offset = sum(past_sizes)
        struct_type = referenced_struct.fields[field_idx].type
        total_field_offset += field_offset
        
    output_type = struct_type
    output_field_size = get_size(output_type, structs)

    # gets the actual assembly now that the field position and size is known
    [assembly, _] = get_leaf_assembly(inner_node, is_target, total_field_offset, output_field_size, variables, structs)

    # for a function call it's gonna return the entire struct regardless
    # so then i have to retrieve the part of the struct for the given field
    if type(inner_node) is Function_Call:
        inner_node_output_type = get_function_output_type(inner_node.function_name)
        
        inner_node_output_size = get_size(inner_node_output_type, structs)        
        final_output_size = get_size(output_type, structs)
        
        assembly.append("; retrieve field from function call output")
        assembly += prepare_indirect_from_stack_pointer()

        #FLIPPED plus totalfieldoffset
        # load_offset = inner_node_output_size - total_field_offset
        load_offset = total_field_offset + final_output_size
        store_offset = inner_node_output_size
        # load from where it is originally on the stack
        # then store where it should be right above everything else
        for byte_idx in range(final_output_size):
            assembly += load_indirect_sp_with_offset(load_offset - byte_idx)
            assembly += store_indirect_sp_with_offset(store_offset - byte_idx)
            
        # pop back so the SP is now right above the field
        n_pops_to_drop = inner_node_output_size - final_output_size
        for _ in range(n_pops_to_drop):
            assembly.append(pop())

    return [assembly, output_type]



def get_sizeof(sizeof_argument, variables: list[list[Variable_Allocated]], structs: list[list[Struct]]) -> int:
    
    """
    i find it kind of weird that an array literal size of the total size of the actual items even though it's essentially a pointer
    but whatever
    """

    reversed_variables = flatten(variables)
    reversed_variables.reverse()

    for variable in reversed_variables:

        if type(sizeof_argument) is not VARIABLE: break

        assert type(variable) is Variable_Allocated

        is_array = variable.type.base_type == Base_Types.ARRAY_PLACEHOLDER
        is_name = variable.name == sizeof_argument.name

        if is_array and is_name:
            return variable.size

    
    


    
    [_, output_type] = get_expression_assembly(sizeof_argument, variables, structs)
    




    expression_size = get_size(output_type, structs)

    return expression_size



my_own_intrinsic_function_names = ["_print_char", "_print_int","_halt"]

def get_function_call_assembly(function_call: Function_Call, variables: list[list[Variable_Allocated]], structs: list[list[Struct]]) -> list[Any]:

    
    """
    steps for function call
        pushes the arguments on the stack (push placeholders if return size is larger)
        pushes the base pointer on the stack
        pops the base pointer back to its spot
        gets the output to the TOS

    """




    

    if function_call.function_name in my_own_intrinsic_function_names:
        
        if function_call.function_name == "_halt":
            halt_assembly = ["jmp halt_point"]
            return [halt_assembly, Type(Base_Types.INT8, 0)]


        # prints the low byte of the argument
        print_assembly: list[str] = []

        if len(function_call.arguments) != 1:
            raise ArgumentMismatchException(f"{function_call.function_name} magic function only accepts 1 argument")
        
        print_argument = function_call.arguments[0]
        [expression_assembly, output_type] = get_expression_assembly(print_argument, variables, structs)
        expression_size = get_size(output_type, structs)
        print_assembly += expression_assembly

        if function_call.function_name == "_print_char":
            if expression_size == 1: instruction_name = "_print_char"
            else: raise ArgumentMismatchException("printchar can only be 1 byte")
        elif function_call.function_name == "_print_int":
            if expression_size == 1: instruction_name = "_print_int8"
            elif expression_size == 2: instruction_name = "_print_int16"
            else: raise ArgumentMismatchException("printint can only be 1 or 2 bytes")
        

        pop_argument_assembly = [pop()] * expression_size

        match TARGET:
            case Target.AVR:
                # for the avr emulator, i'm retrieving from the top of stack
                print_assembly.append(instruction_name)
                print_assembly += pop_argument_assembly
            case Target._6502:
                # for 6502 i'm jumping to a subroutine that takes the char from the accumulator
                print_assembly += pop_argument_assembly
                if instruction_name == "_print_char":
                    print_assembly.append(f"jsr _print_char")





    

        # returning an int8 with value 0 is totally arbitrary
        print_assembly += [
            load_immediate(0),
            push()
            # f"ldi {TEMP_REG}, 0",
            # f"push {TEMP_REG}"
        ]
        return [print_assembly, Type(Base_Types.INT8,0)]
    
    elif function_call.function_name == "sizeof":
        if len(function_call.arguments) != 1:
            raise ArgumentMismatchException(f"{function_call.function_name} magic function only accepts 1 argument")
        
        sizeof_argument = function_call.arguments[0]



        expression_size = get_sizeof(sizeof_argument, variables, structs)
        
        sizeof_assembly = [
            load_immediate(expression_size),
            push()
        ]
        
        return [sizeof_assembly, Type(Base_Types.INT8,0)]


    assert type(function_call) is Function_Call
    parameters = get_function_parameters(function_call.function_name)
    output_type = get_function_output_type(function_call.function_name)
    if len(parameters) != len(function_call.arguments):
        raise ArgumentMismatchException()

    total_parameter_size = sum([get_size(parameter.type, structs) for parameter in parameters])
    return_size = get_size(output_type, structs)
    space_after_parameters_size = max(0, return_size-total_parameter_size)
    space_after_output_size = max(0, total_parameter_size - return_size)

    assembly = []

    string_type = Type(Base_Types.INT8, 1)
    string_size = 2
    assert get_size(string_type, structs) == string_size


    """
    REFACTOR this is scary
    but maybe there's nothing i can do about it
    if an argument is a string literal it puts all the chars on the stack
    that messes up where in the stack to look for arguments
    so instead i get the string assembly FIRST and create a dummy variable that points to the string
    i then load that dummy variable from the stack when pushing the arguments

    dummy names are not unique over multiple calls to the same function
    however this still works since im using allocatetostack (which doesnt check for duplicate names)
        (allocatevariabletostack checks)
    getvariableasm then gets the most recent variable with that name, doesnt care about duplicates
    """
    
    @dataclass
    class String_Argument:
        variable: VARIABLE
        argument_idx: int

    string_arguments: list[String_Argument] = []
    
    for (argument_idx, argument) in enumerate(function_call.arguments):
        if type(argument) is not STRING: continue
        string_assembly = get_string_assembly(argument, variables, structs)
        assembly += string_assembly
        dummy_name = f"__STRING_IN_CALL__{function_call.function_name}_{argument_idx}"
        dummy_variable = VARIABLE(dummy_name)
        allocate_to_stack(string_size, dummy_name, string_type, variables)
        string_arguments.append(String_Argument(dummy_variable, argument_idx))
        





    # push all the parameters to the stack
    for idx, argument in enumerate(function_call.arguments):
        parameter = parameters[idx]
        assert type(parameter) is Variable_Typed
        
        if type(argument) is STRING:
            matched_arguments = [arg for arg in string_arguments if arg.argument_idx == idx]
            assert len(matched_arguments) == 1
            string_argument = matched_arguments[0]
            [argument_assembly, argument_type] = get_variable_assembly(string_argument.variable, False, 0, None, variables, structs)
            assert types_match(argument_type, string_type)
        else:
            [argument_assembly, argument_type] = get_expression_assembly(argument, variables, structs)



        if not types_match(parameter.type, argument_type):
            raise TypeException(f"argument parameter mismatch for {parameter.name}")
        assembly += argument_assembly
        assembly += get_size_match_assembly(parameter.type, argument_type, structs)



    # placeholders are needed so there's enough space for it to return
    if space_after_parameters_size > 0:
        assembly.append("")
        assembly.append("; fill in placeholders since output size is more than parameters")
        # doesn't matter what value you push, but im going with 0 so it's easier to debug the asm
        assembly.append(load_immediate(0))
        # assembly.append(f"ldi {TEMP_REG}, 0")
    for _ in range(space_after_parameters_size):
        assembly.append(push())
        # assembly.append(f"push {TEMP_REG}")


    
    store_base_pointer_assembly = [

        "",
        "; push BP, call, then store BP back",
        load_from_memory(BP_LOW),
        push(),
        load_from_memory(BP_HIGH),
        push(),
        # f"lds {TEMP_REG}, {BP_ADDRESS_LOW}",
        # f"push {TEMP_REG}",
        # f"lds {TEMP_REG}, {BP_ADDRESS_HIGH}",
        # f"push {TEMP_REG}",
        
    ]
    assembly += store_base_pointer_assembly
    assembly.append(call_subroutine(function_call.function_name))
    # load_base_pointer_assembly = [
    #     pop(),
    #     store_to_memory(BP_HIGH),
    #     pop(),
    #     store_to_memory(BP_LOW),

        
    # ]


    load_base_pointer_assembly = [
        "sec",
        pop(),
        "tax",
        pop(),
        f"sta {BP_LOW}",
        f"sbc #{OFFSET_TEST}",
        f"sta {LOW_INDIRECT_6502_BP}",
        "txa",
        f"sbc #0",
        f"sta {HIGH_INDIRECT_6502_BP}"
    ]








    assembly += load_base_pointer_assembly

    # the output is put to the top of the spot, so if the parameters are larger the output needs to get put to the bottom
    # almost identical code to accessing a field from a function call
    if space_after_output_size > 0:
        assembly += [
            "",
            "; retrieve field from function call output",
            
        ]
        assembly += prepare_indirect_from_stack_pointer()

        load_offset = return_size
        store_offset = total_parameter_size
        # load from where it is originally on the stack
        # then store where it should be right above everything else
        for byte_idx in range(return_size):
            assembly += load_indirect_sp_with_offset(load_offset - byte_idx)
            assembly += store_indirect_sp_with_offset(store_offset - byte_idx)
            
        # pop back so the SP is now right above the return
        n_pops_to_drop = space_after_output_size
        for _ in range(n_pops_to_drop):
            assembly.append(pop())

    return [assembly, output_type]


def get_array_index_assembly(leaf: Array_Index, is_target: bool, struct_field_offset: int, struct_field_size: int, variables: list[list[Variable_Allocated]], structs: list[list[Struct]]) -> list[Any]:

    """
    gets the assembly for indexing an array
        push the array and index
        subtracts and loads/stores at that address
    struct offset and field size are for only accessing one part of an array element
        a[b].c  should only load/store the c field of a[b]
        
    leaf: tree node 
    is_target: says if it's a load or store, only true if the index is at the top level of an assignment
    struct_field_offset: how far the start of the desired field is from the start of the struct (0 if it's the first field)
    struct_field_size: size of field 
    """

    [_, array_type] = get_leaf_assembly(leaf.array, False, 0, None, variables, structs)
    assert type(array_type) is Type
    if array_type.reference_level == 0:
        raise TypeException("cannot index something that's not a pointer to something else")
    
    output_type = Type(array_type.base_type, array_type.reference_level - 1)
    element_size = get_size(output_type, structs)


    is_zero_index = type(leaf.index) is NUMBER and leaf.index.value == 0

    type_cast_tree = Type_Cast(leaf.array,Type(Base_Types.INT16,0))

    artificial_index_tree: Tree
    
    if is_zero_index:
        artificial_index_tree = type_cast_tree
    else:
        artificial_index_tree = \
        Operation(
            type_cast_tree,
            PLUS(),
            Operation(
                leaf.index,
                ASTERISK(),
                NUMBER(element_size)
            )
        )


    assembly = []

    [offset_assembly, offset_type] = get_expression_assembly(artificial_index_tree, variables, structs)
    assembly += offset_assembly

    assert type(offset_type) is Type
    assert offset_type.base_type is Base_Types.INT16 and offset_type.reference_level == 0, "subtraction with int16 should produce int16"


    match TARGET:
        case Target.AVR:
            prepare_indirect_assembly = [
                f"pop {X_HIGH}",        # high pointer
                f"pop {X_LOW}",         # low pointer
            ]
        case Target._6502:
            prepare_indirect_assembly = [
                "pla",
                f"sta {HIGH_INDIRECT_6502_ARRAY}",
                "pla",
                f"sta {LOW_INDIRECT_6502_ARRAY}",
            ]

    assembly += prepare_indirect_assembly


    # none means access everything, otherwise just access the field
    if struct_field_size is None:
        n_bytes_to_access = element_size
    else:
        n_bytes_to_access = struct_field_size

    # load/store the desired bytes
    # this is very similar to loadfromstack and storetostack
    # it's fine though
    if is_target:
        # if it's target, the expression would be at the TOS, to be stored at the right spot
        #FLIPPED for storing go from 0 to n
        # for byte_idx in range(n_bytes_to_access-1,-1,-1):
        for byte_idx in range(n_bytes_to_access):
            assembly += [
                pop(),
                # f"pop {TEMP_REG}",
                #FLIPPED add from X, keep adding the structoffset+byteidx
                # f"std X-{struct_field_offset+byte_idx}, {TEMP_REG}"
                # f"std X+{struct_field_offset+byte_idx}, {TEMP_REG}"
            ]
            assembly += store_indirect_with_offset_array(struct_field_offset + byte_idx)
    else:
        # for an expression, push the result to the TOS
        # FLIPPED for loading go from n-1 to -1
        # for byte_idx in range(n_bytes_to_access):
        for byte_idx in range(n_bytes_to_access-1,-1,-1):
            assembly += load_indirect_with_offset_array(struct_field_offset+byte_idx)
            assembly += [
                #FLIPPED add from X, keep adding the structoffset+byteidx
                # f"ldd {TEMP_REG}, X-{struct_field_offset+byte_idx}",
                # f"ldd {TEMP_REG}, X+{struct_field_offset+byte_idx}",
                push()
                # f"push {TEMP_REG}"
            ]

    return [assembly, output_type]



def get_leaf_assembly(expression: Tree, is_target: bool, struct_field_offset: int, struct_field_size: int, variables: list[list[Variable_Allocated]], structs: list[list[Struct]]) -> list[Any]:
                            

    """
    the idea is this only for things that you can assign something to (where istarget is true)
    but in that case function calls really shouldn't be included
    REFACTOR not sure if this should be a function at all

    expression: tree node 
    is_target: says if it's a load or store, only true if the index is at the top level of an assignment
    struct_field_offset: how far the start of the desired field is from the start of the struct (0 if it's the first field)
    struct_field_size: size of field 
    """
    if type(expression) is VARIABLE:
        return get_variable_assembly(expression, is_target, struct_field_offset, struct_field_size, variables, structs)
    elif type(expression) is Function_Call:
        return get_function_call_assembly(expression, variables, structs)
    elif type(expression) is Array_Index:
        return get_array_index_assembly(expression, is_target, struct_field_offset, struct_field_size, variables, structs)
    elif type(expression) is Struct_Field:
        return get_struct_field_assembly(expression, is_target, variables, structs)
    else:
        # TODO check exactly what causes this to get hit
        raise ParseException()
    


def get_expression_assembly(expression: Tree, variables: list[list[Variable_Allocated]], structs: list[list[Struct]]) -> list[Any] :

    """
    general function for any expression
    used for assignment target, assignment expression, declaration expression, return, array items, array indices, operation etc.
    """

    assembly = []


    if type(expression) is NULL_KEYWORD:
        assembly += [
            f"; store null",
            load_immediate(0),
            push(),
            push(),
        ]
        output_type = Type(Base_Types.INT8, 1)
    elif type(expression) is NUMBER:
        value = expression.value

        assembly += [
            f"; store number"
        ]

        value_low = value % 256
        value_high = int(value/256)

        if value_high == 0:
            assembly += [
                load_immediate(value_low),
                push(),
            ]
            output_type = Type(Base_Types.INT8, 0)
        else:
            assembly += [
                load_immediate(value_low),
                push(),
                load_immediate(value_high),
                push(),
            ]
            output_type = Type(Base_Types.INT16, 0)

    elif type(expression) is CHAR:
        value = ord(expression.value)
        output_type = Type(Base_Types.INT8, 0)
        assembly += [
            "",
            f"; store value {value}",
            load_immediate(value),
        ]    
        assembly.append(push())
    elif type(expression) is STRING:
        assembly += get_string_assembly(expression, variables, structs)
        output_type = Type(Base_Types.INT8, 1)
    elif type(expression) is Reference:
        referenced_variable = get_variable(expression.variable_name, variables)
        offset = referenced_variable.base_pointer_offset
        if offset > 255: raise NotImplementedYetException()
        assembly += [
            "",
            f"; get the reference of {expression.variable_name}",
            load_from_memory(BP_LOW),
            # f"lds {TEMP_REG}, {BP_ADDRESS_LOW}",
        ]
        assembly += subtract_immediate(offset)
        assembly += [
            push(),
            load_from_memory(BP_HIGH),
            subtract_immediate_with_carry(0),
            push()
        ]
        
        variable_type = referenced_variable.type
        assert type(variable_type) is Type
        output_type = Type(variable_type.base_type, variable_type.reference_level+1)
    
    elif type(expression) is Type_Cast:

        [assembly, input_type] = get_expression_assembly(expression.node, variables, structs)
        output_type = expression.casted_type
        assembly += get_size_match_assembly(output_type, input_type, structs)

    elif type(expression) is UnitaryOperation:
        assert type(expression.operation) is NOT, "i added another unitary operation?"
        [not_assembly, output_type] = get_not_assembly(expression, variables, structs)
        assembly += not_assembly

    elif type(expression) is Operation and type(expression.operation) in [PLUS,MINUS, BIT_AND, BIT_OR]:
        [add_assembly, output_type] = get_add_subtract_assembly(expression, variables, structs)
        assembly += add_assembly
    elif type(expression) is Operation and type(expression.operation) in [GREATER_THAN, LESS_THAN, GREATER_EQUAL, LESS_EQUAL]:
        [inequality_assembly, output_type] = get_inequality_assembly(expression,variables, structs)
        assembly += inequality_assembly
    elif type(expression) is Operation and type(expression.operation) in [EQUAL_COMPARE, NOT_EQUAL]:
        [equal_assembly, output_type] = get_equality_assembly(expression, variables, structs)
        assembly += equal_assembly
    elif type(expression) is Operation and type(expression.operation) in [AND, OR]:
        [and_or_assembly, output_type] = get_and_or_assembly(expression, variables, structs)
        assembly += and_or_assembly
    elif type(expression) is Operation and type(expression.operation) is ASTERISK:
        [multiply_assembly, output_type] = get_multiply_assembly(expression, variables, structs)
        assembly += multiply_assembly
    elif type(expression) is Operation and type(expression.operation) is DIVIDE:
        raise NotImplementedYetException("divide not supported yet")
    elif type(expression) in [VARIABLE, Function_Call, Array_Index, Struct_Field]:
        [leaf_assembly, output_type] = get_leaf_assembly(expression, False, 0, None, variables, structs)
        assembly += leaf_assembly
    else:
        assert False, "expression can only contain operations, numbers, and variables, what's going on?"
        
    # REFACTOR not sure if this is the best place or if this is the check i wanna do
    if type(expression) is Operation and expression.operation in [PLUS, MINUS, ASTERISK, DIVIDE]:
        if not is_int_type(expression.operand1, variables, structs):
            raise TypeException(f"{expression.operand1} isn't an int, required for {expression.operation}")
        if not is_int_type(expression.operand2, variables, structs):
            raise TypeException(f"{expression.operand2} isn't an int, required for {expression.operation}")
    
    assert type(output_type) is Type
    return [assembly, output_type]




def get_declaration_assembly(declaration: Declaration, variables: list[list[Variable_Allocated]], structs: list[list[Struct]]) -> list[Any]:

    """
    allocates the target and generates the assembly for the RHS
    """

    assert type(declaration) is Declaration
    assembly = [
        "",
        "; get declaration:"
    ]
    target = declaration.target
    expression = declaration.RHS
    assert type(target) is Variable_Typed, "i thought declarations only target variables"
    output_size = get_size(target.type, structs)



    size_match_assembly: list[str] = []

    is_uninitialized = expression is None
    if is_uninitialized:
        expression_assembly = [
            "",
            f"; defaulting uninitialized {target.name} to 0",
            load_immediate(0),
            
        ]
        expression_assembly += [push()] * output_size
    elif type(expression) is Array_Literal:
        [expression_assembly, expression_type] = get_array_assembly(target, expression, variables, structs)
    else:
        [expression_assembly, expression_type] = get_expression_assembly(expression, variables, structs) 
        if not is_uninitialized and not types_match(target.type,expression_type):
            raise TypeException(f"expression type for declaration of {target.name} doesn't match")
        size_match_assembly = get_size_match_assembly(target.type, expression_type, structs)


    assembly += expression_assembly
    assembly += size_match_assembly    
    
    allocate_variable_to_stack(target, variables, structs, None)



    return assembly



def get_assignment_assembly(assignment: Assignment, variables: list[list[Variable_Allocated]], structs: list[list[Struct]]) -> list[Any]:

    
    """
    pushes the RHS to the stack
    then stores in the target's location
    """

    assert type(assignment) is Assignment
    assembly = [
        "",
        f"; assign variable:"
    ]

    expression = assignment.RHS
    [expression_assembly, expression_type] = get_expression_assembly(expression, variables, structs)
    assembly += expression_assembly

    
    target = assignment.target
    [target_assembly, target_type] = get_leaf_assembly(target, True, 0, None, variables, structs)
    size_match_assembly = get_size_match_assembly(target_type, expression_type, structs)
    
    
    assembly += size_match_assembly
    assembly += target_assembly


    if not types_match(expression_type, target_type):
        raise TypeException(f"type mismatch for {target}")
    

    return assembly
    


@dataclass
class Scope_Space:
    space: int
    is_loop: bool
    loop_continue_label: str|None
    loop_break_label: str|None


scope_spaces: list[Scope_Space] = []


"""
i can lump the continue point, break point, and depth globals in with the scopespace

function
    reset scope_spaces at start of function

allocate_to_stack (includes declarations, arrays, strings)
    if scopespaces is empty no need to do anything
    otherwise add to the last scopespace space by the size of the declaration


if statements/non loop scopes
    at the start of each case append a new scopespace (isloop=False)
    at the end of each case
        pop the total amoutn of space
        remove it

    
while/for loop scopes
    at the start append a new scopespace (isloop=True)
    at each iteration reset space to 0
    at the end remove it

continue and break
    traverse backard until there's one where isloop = True
    accumulate the total space, including the one where isloop = True
    pop that number of spaces

return
    no need to do anything
    the basepointer will reset the stack pointer back to where it belongs

    

"""



# FAST
def get_scope_exit_assembly():

    total_offset_from_bp = 0 
    for scope in scope_spaces:
        total_offset_from_bp += scope.space

    if total_offset_from_bp > 255:
        raise NotImplementedYetException("just need to use the high byte too")


    return set_stack_pointer_from_memory_with_offset(BP_LOW, BP_HIGH, total_offset_from_bp)
    



def get_boolean_assembly(expression: Tree, variables: list[list[Variable_Allocated]], structs: list[list[Struct]]) -> list[Any]:

    """
    checks if the thing on TOS is true (something is nonzero)
    
    """


    output_type = Type(Base_Types.INT8, 0)

    assembly: list[str] = []


    [expression_assembly, expression_type] = get_expression_assembly(expression, variables, structs)
    expression_size = get_size(expression_type, structs)

    assembly += expression_assembly


    if expression_size == 1:
        # if it's one byte, the TOS already has the value (not 0 means true)
        return [assembly, output_type]

    is_true_point = get_jump_point("bool_true")
    exit_point = get_jump_point("bool_exit")

    for _ in range(expression_size):
        assembly += [
            pop(),
            compare_immediate(0),
        ]
        assembly += branch_not_equal(is_true_point)

    assembly += [
        load_immediate(0),
        f"jmp {exit_point}",
        f"{is_true_point}:",
        load_immediate(1),
        f"{exit_point}:",
        push(),
    ]

    return [assembly, output_type]


def get_if_statement_assembly(if_container: If_Container, variables: list[list[Variable_Allocated]], structs: list[list[Struct]]) -> list[str]:
    
    assert type(if_container) is If_Container

    assembly: list[str] = []

    label_end = get_jump_point("if_end")

    for block in if_container.blocks:
    
        if_scope = Scope_Space(0, False, None, None)
        scope_spaces.append(if_scope)


        label_skip = get_jump_point("if_skip")
        [condition_assembly, _] = get_boolean_assembly(block.condition, variables, structs)
        assembly += condition_assembly
        assembly += [
            pop(),
            compare_immediate(0),

        ]
        
        assembly += branch_equal(label_skip)
        assembly += get_block_assembly(block.block, variables, structs)
        assembly.append(f"jmp {label_end}")
        assembly.append(f"{label_skip}:")

        scope_spaces.pop()


    
    assembly.append(f"{label_end}:")
    assembly += get_scope_exit_assembly()
        
    return assembly





def get_while_loop_assembly(while_block: While_Block, variables: list[list[Variable_Allocated]], structs: list[list[Struct]]) -> list[str]:
    


    assert type(while_block) is While_Block
    assembly = []
    continue_jump_point = get_jump_point("while_continue")
    loop_jump_point = get_jump_point("while_loop")
    exit_jump_point = get_jump_point("while_exit")
    


    exit_assembly = get_scope_exit_assembly()

    while_scope = Scope_Space(0, True, continue_jump_point, exit_jump_point)
    scope_spaces.append(while_scope)

    assembly.append(f"{loop_jump_point}:")
    [condition_assembly, _] = get_boolean_assembly(while_block.condition, variables, structs)
    assembly += condition_assembly
    assembly.append(pop())
    assembly.append(compare_immediate(0))
    assembly += branch_equal(exit_jump_point)
    block_assembly = get_block_assembly(while_block.block, variables, structs)
    assembly += block_assembly
    assembly.append(f"{continue_jump_point}:")
    assembly += exit_assembly
    
    assembly.append(f"jmp {loop_jump_point}")
    assembly.append(f"{exit_jump_point}:")
    assembly += exit_assembly

    scope_spaces.pop()

    return assembly




def get_for_loop_assembly(for_block: For_Block, variables: list[list[Variable_Allocated]], structs: list[list[Struct]]) -> list[str]:
    
    assert type(for_block) is For_Block
    assembly = []
    loop_jump_point = get_jump_point("for_loop")
    continue_jump_point = get_jump_point("continue_loop")
    exit_jump_point = get_jump_point("for_exit")
    


    exit_assembly = get_scope_exit_assembly()

    for_scope = Scope_Space(0, True, continue_jump_point, exit_jump_point)
    scope_spaces.append(for_scope)

    assembly += get_assignment_assembly(for_block.initializer, variables, structs)
    assembly.append(f"{loop_jump_point}:")
    [condition_assembly, _] = get_boolean_assembly(for_block.condition, variables, structs)
    assembly += condition_assembly
    assembly.append(pop())
    assembly.append(compare_immediate(0))
    assembly += branch_equal(exit_jump_point)
    assembly += get_block_assembly(for_block.block, variables, structs)
    assembly.append(f"{continue_jump_point}:")

    assembly += exit_assembly

    assembly += get_assignment_assembly(for_block.incrementer, variables, structs)
    assembly.append(f"jmp {loop_jump_point}")
    assembly.append(f"{exit_jump_point}:")
    

    assembly += exit_assembly


    scope_spaces.pop()

    return assembly

def get_function_assembly(function_block: Function_Block, variables: list[list[Variable_Allocated]], structs: list[list[Struct]]) -> list[str]:

    """
    asm does function stuff
        sets the BP
        pushes and allocates parameters, like with declarations
        does the function code
        default return (returns stored at the top of the parameter/return spot below SP and BP)
    the caller is responsible for storing the parameters, and shuffling the return to the bottom of the spot if needed
    """
    if function_block.name in my_own_intrinsic_function_names:
        # this is so that i can have _print_int or _print_char contain calls to printf
        # that way gcc can compile it and everything runs the same
        return []

    assembly = []

    assert type(function_block) is Function_Block
    n_scopes = len(variables)
    assert n_scopes == 1, "i thought functions had to be outermost blocks"
    for reached_function in functions_reached:
        if reached_function.name == function_block.name:
            raise RepeatedDeclarationException(f"multiple functions with same name: {function_block.name}")
    functions_reached.append(function_block)
    # ensure the function asm only gets executed when the function is called
    skip_function_point = get_jump_point(f"{function_block.name}_skip")
    
    scope_spaces.clear()
    scope_spaces.append(Scope_Space(0, False, None, None))


    assembly.append(f"jmp {skip_function_point}")
    assembly.append(f"{function_block.name}:")


    # FAST - no longer needed, no longer using base pointer
    # the new base is right above the SP address pushed by the call
    assembly += [
        "",
        "; store the stack pointer into the base pointer:"
    ]
    # assembly += set_memory_from_stack_pointer(BP_LOW, BP_HIGH)
        
    assembly += [
        "sec",
        "tsx",
        f"stx {BP_LOW}",
        "txa",
        f"sbc #{OFFSET_TEST}",
        f"sta {LOW_INDIRECT_6502_BP}",
        f"lda #1",
        "sbc #0",
        f"sta {HIGH_INDIRECT_6502_BP}"

    ]



    parameter_sizes = [get_size(parameter.type, structs) for parameter in function_block.parameters]
    total_parameter_size = sum(parameter_sizes)
    output_size = get_size(function_block.output_type, structs)
    total_size = max(total_parameter_size, output_size)

    if total_parameter_size > 0:
        stack_pointer_offset = 2
        base_pointer_offset = 2
        cumulative_offset = stack_pointer_offset + base_pointer_offset + total_size + 1
        for size, parameter in zip(parameter_sizes, function_block.parameters):
            cumulative_offset -= size
            assert type(parameter) is Variable_Typed
            allocate_variable_to_stack(parameter, variables, structs, cumulative_offset)
        
        
        
    # actually do the function
    assembly += get_block_assembly(function_block.block, variables, structs)
    
    # default 0 return
    assembly += [
        "",
        "; default return value of 0",
        load_immediate(0)
    ]
    for _ in range(output_size):
        assembly.append(push())


    assembly += get_return_assembly(output_size)
    
    assembly.append(f"{skip_function_point}:")
    return assembly


def get_return_assembly(output_size: int) -> list[str]:

    """
    assumes the output is stored on the top of the stack
    moves it back into the proper slot
    this slot is at the top part of the parameter/output placeholder
        if the parameters take more size, the caller then shuffles the output back down
    then pops back to the PC
    needs to be its own function cause it's called both for explicit returns and default returns at the end of a function
    """

    return_assembly = []

    stack_pointer_offset = 2
    base_pointer_offset = 2

    return_assembly.append("")
    return_assembly.append("; store output bytes back where it can be retrieved by the caller:")
    for byte_idx in range(output_size):
        # four back would take it to the start of the stack pointer
        # need to add one more to get before there
        offset = stack_pointer_offset + base_pointer_offset + byte_idx + 1
        # return_assembly += [
        #     pop()
        # ]
        return_assembly.append(pop())
        return_assembly += store_indirect_with_offset_bp(offset)
        
    return_assembly += set_stack_pointer_from_memory(BP_LOW, BP_HIGH)
    return_assembly.append(return_from_subroutine())
    return return_assembly


def get_current_loop_scope() -> Scope_Space:
    reversed_scopes = scope_spaces.copy()
    reversed_scopes.reverse()

    for scope in reversed_scopes:
        if scope.is_loop:
            return scope
        
    assert False, "a break or continue is outside of a loop, should have been caught in parsing"

    

def get_block_assembly(lines: list[list[Block]], variables: list[list[Variable_Allocated]], structs: list[list[Struct]]) -> list[str]:

    """
    this is the block of lines itself
    so for 
        if(1){int a = 4; int b = 5;}

    it's getting the asm for just
    [int a=4, int a=5]
    NOT the entire if statement    
    """


    assert type(lines) is list
    assembly = []
    block_asm_functions = {
        If_Container: get_if_statement_assembly,
        While_Block: get_while_loop_assembly,
        For_Block: get_for_loop_assembly,
        Function_Block: get_function_assembly
    }
    has_main = False

    in_global_scope = len(variables) == 0
    if in_global_scope:
        match TARGET:
            case Target.AVR:
                assembly += [
                    ".global main",
                    "",
                    "; set the global pointer to the initial stack pointer",
                ]
            case Target._6502:
                assembly += [
                    "PCR = $600C",
                    "IFR = $600D",
                    "IER = $600E",
                    f"{BP_LOW} = {BP_LOW_ADDRESS}",
                    f"{BP_HIGH} = {BP_HIGH_ADDRESS}",
                    f"{GLOBAL_P_LOW} = {GLOBAL_P_LOW_ADDRESS}",
                    f"{GLOBAL_P_HIGH} = {GLOBAL_P_HIGH_ADDRESS}",
                    f"{LOW_INDIRECT_6502_BP} = {LOW_INDIRECT_6502_ADDRESS_BP}",
                    f"{HIGH_INDIRECT_6502_BP} = {HIGH_INDIRECT_6502_ADDRESS_BP}",
                    f"{LOW_INDIRECT_6502_GP} = {LOW_INDIRECT_6502_ADDRESS_GP}",
                    f"{HIGH_INDIRECT_6502_GP} = {HIGH_INDIRECT_6502_ADDRESS_GP}",
                    f"{LOW_INDIRECT_6502_ARRAY} = {LOW_INDIRECT_6502_ADDRESS_ARRAY}",
                    f"{HIGH_INDIRECT_6502_ARRAY} = {HIGH_INDIRECT_6502_ADDRESS_ARRAY}",
                    f"{RIGHT_SIDE_6502} = {RIGHT_SIDE_6502_ADDRESS}",
                    ".org $8000",
                    "reset:",
                    "cld",
                    "cli", 
                    "lda #%10011011 ; allow via to handle interrupts",
                    "sta IER",
                    "ldx #$ff",
                    "txs",
                    "; the high base pointer will always be 1:",
                    "lda #1",
                    f"sta {BP_HIGH}",
                    "; falling edge interrupt",
                    "lda #$00",
                    "sta PCR"
                ]
                
                    
        # FAST - no longer using global pointer
        assembly += set_memory_from_stack_pointer(GLOBAL_P_LOW, GLOBAL_P_HIGH)
        assembly += prepare_indirect_from_memory_with_offset(OFFSET_TEST, True)

    for line in lines:
        if type(line) is Function_Block and line.name == "main":
            has_main = True
        
        
        if type(line) in block_asm_functions.keys():
            block_variables = variables.copy()
            block_variables.append([])   # for the new scope
            block_structs = structs.copy()
            block_structs.append([])   # for the new scope
            assembly += block_asm_functions[type(line)](line, block_variables, block_structs)
        elif type(line) is Assignment:
            assembly += get_assignment_assembly(line, variables, structs)
        elif type(line) is Declaration:
            assembly += get_declaration_assembly(line, variables, structs)
        elif type(line) is Return:
            assert len(functions_reached) != 0, "a function would have had to been added to have been in return"
            current_function = functions_reached[-1]
            assert type(current_function) is Function_Block
            
            if line.value is None:
                raise NotImplementedYetException("must return a value")
            ## FUTURE allow return; ?
            [return_expression_assembly, return_type] = get_expression_assembly(line.value, variables, structs)
            
            assert type(return_type) is Type

            if not types_match(return_type,current_function.output_type):
                raise TypeException("return output type no match")
            


            assembly += return_expression_assembly
            assembly += get_size_match_assembly(current_function.output_type, return_type, structs)
            
            output_size = get_size(current_function.output_type, structs)
            assembly += get_return_assembly(output_size) 
        elif type(line) is BREAK_KEYWORD:
            assembly.append(f"jmp {get_current_loop_scope().loop_break_label}")
        elif type(line) is CONTINUE_KEYWORD:
            assembly.append(f"jmp {get_current_loop_scope().loop_continue_label}")

        elif type(line) is Struct:
            save_struct_in_scope(line, structs)
        else:
            [expression_assembly, output_type] = get_expression_assembly(line, variables, structs)
            assembly += expression_assembly
            assembly.append("; pop unused expression ouput:")
            assembly += [pop()] * get_size(output_type, structs)
        
    
    if in_global_scope and not has_main:
        raise ParseException("main isn't one of the functions")
    if in_global_scope:
        base_pointer_offset = 2
        main_function_call = Function_Call("main", [])
        
        # assembly += [
        #     "",
        #     "; hack just to get the output top byte to the temp reg",
        #     call_subroutine("main"),
        # ]
        assembly += get_function_call_assembly(main_function_call, variables, structs)[0]

        assembly += prepare_indirect_from_stack_pointer()
        # assembly += load_indirect_with_offset(base_pointer_offset+1)
        assembly += load_indirect_sp_with_offset(1)
        assembly += [f"halt_point:"]
        if TARGET is Target._6502:
            assembly += [
                "sta $4000; for the emulator to know to halt",
                "jmp halt_point; so the actual computer will stay in a loop",
            ]
            

            assembly.append("irq_jump_point:")
            assembly += """
  pha
  txa
  pha
  tya
  pha

  lda IFR
  ; selecting the correct option based on thing that interrupted would happen here
    ;lda #%00011011
  ;sta IER

""".split("\n")
            
            irq_function_call = Function_Call("irq", [])
            assembly += get_function_call_assembly(irq_function_call, variables, structs)[0]
            # assembly.append("cli")
            assembly += """
  ; the pull is cause normally the output would be consumed
  pla


  
  ;lda #%10011011
  ;sta IER
  bit $6000
  bit $6001
  pla
  tay
  pla
  tax
  pla
  rti
""".split("\n")
            
                

            assembly += [

                ".org $fffa",
                ".word irq_jump_point",
                ".org $fffc",
                ".word reset",
                ".org $fffe",
                ".word irq_jump_point",
                
            ]
            
    return assembly

def get_assembly(tree: Tree) -> str:

    assembly_lines: list[str] = []

    assembly_lines += get_block_assembly(tree, [], [[]])

    if TARGET == Target._6502:
        for idx, line in enumerate(assembly_lines):
            if ":" in line:
                assert line.endswith(":")
            elif "=" in line: pass
            else:
                assembly_lines[idx] = f"{' '*4}{line}"
    assembly = "\n".join(assembly_lines)
    return assembly

def compile(file_name: str) -> str:

    ## REFACTOR the tree is just global cause of a stupid hack where i use it to get function output types and parameters
    # fix this
    global syntax_tree

    with open(file_name) as f:
        characters_raw = f.read()

    characters = preprocess(characters_raw, [file_name])
    all_tokens = lex_text(characters)
    syntax_tree = parse_code(all_tokens)
    assembly = get_assembly(syntax_tree)

    if __name__ == "__main__":
        print(all_tokens)
        print("\n")
        print("\n")
        print(assembly)


    
    return assembly



if __name__ == "__main__":
    # file_name = sys.argv[1]
    
    assembly = compile("mini_test.c")


    with open("main.S","w") as f:
        f.write(assembly)