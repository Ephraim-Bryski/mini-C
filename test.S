reset:
    jsr _print_char
    sta $4000

    .org $fffa
    .word reset