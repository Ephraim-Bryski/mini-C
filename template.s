    .org $8000
reset:

    ldx #$ff
    txs
    cld

    ; code here

halt_point:
    sta $4000
    jmp halt_point
    
  .org $fffc
  .word reset