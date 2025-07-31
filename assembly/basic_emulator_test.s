
PORTB = $6000
PORTA = $6001

E =  %10000000
RW = %01000000
RS = %00100000

    .org $8000
    lda #2
    
reset:


    lda #"H"
    jsr print_char
    lda #"i"
    jsr print_char
    lda #"!"
    jsr print_char

    jmp end

print_char:

    sta PORTB
    lda #RS
    sta PORTA
    lda #(RS|E)
    sta PORTA
    lda #RS
    sta PORTA
    rts

end:

    sta $4000


    .org $fffc
    .word reset