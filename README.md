Just for fun, for learning about hardware and low-level software.\
The compiler is written in Python, compiles a subset of C, and targets 6502 assembly.\
Mini-C supports:
* Branches, loops, and functions (with recursion)
* Math with order of operations
* Types: char (8 bit), int (16 bit), arrays, strings, and structs
* Nested data structures (e.g. arrays of structs)
* Pointer reference and dereference (zero index for dereference)

There's also an assembler and emulator, used for a test suite.

I have a small library of programs written in mini-C, including a basic memory allocator. The library also includes routines for interfacing with the LCD in Ben Eater's 6502. I was able to run basic programs on the 6502, including an (extremely basic) game, and a very basic text editor (connecting to a ps2 keyboard).
