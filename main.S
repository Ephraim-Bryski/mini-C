PCR = $600C
IFR = $600D
IER = $600E
    .org $8000
reset:
    cld
    cli
    lda #%10011011 ; allow via to handle interrupts
    sta IER
    ldx #$ff
    txs
    ; falling edge interrupt
    lda #$00
    sta PCR
    tsx
    stx 6
    lda #1
    sta 7
    jmp main_skip_0
main:
    
; store the stack pointer into the base pointer:
    tsx
    stx 1
    lda #1
    sta 2
    
    ; store number
    lda #4
    pha
    
    ; store number
    lda #30
    pha
    
    ; store number
    lda #20
    pha
    clc
    tsx
    stx 3
    ldx #1 ; high byte of stack pointer
    stx 4
    
; load indirect:
    ldy #2
    lda (3),Y
    pha
    ldy #1
    lda (3),Y
    sta 5
    pla
    adc 5
    ldy #2
    sta (3),Y
    pla
; pop unused expression ouput:
    pla
    
    ; default return value of 0
    lda #0
    pha
    
; store output bytes back where it can be retrieved by the caller:
    lda 1
    sta 3
    lda 2
    sta 4
    pla
    ldy #5
    sta (3),Y
    lda 1
    tax
    txs
    rts
main_skip_0:
    jmp irq_skip_1
irq:
    
; store the stack pointer into the base pointer:
    tsx
    stx 1
    lda #1
    sta 2
    
    ; default return value of 0
    lda #0
    pha
    
; store output bytes back where it can be retrieved by the caller:
    lda 1
    sta 3
    lda 2
    sta 4
    pla
    ldy #5
    sta (3),Y
    lda 1
    tax
    txs
    rts
irq_skip_1:
    
    ; fill in placeholders since output size is more than parameters
    lda #0
    pha
    
    ; push BP, call, then store BP back
    lda 1
    pha
    lda 2
    pha
    jsr main
    pla
    sta 2
    pla
    sta 1
    tsx
    stx 3
    ldx #1 ; high byte of stack pointer
    stx 4
    
; load indirect:
    ldy #1
    lda (3),Y
halt_point:
    sta $4000; for the emulator to know to halt
    jmp halt_point; so the actual computer will stay in a loop
irq_jump_point:
    
      pha
      txa
      pha
      tya
      pha
    
      lda IFR
      ; selecting the correct option based on thing that interrupted would happen here
        ;lda #%00011011
      ;sta IER
    
    
    
    ; fill in placeholders since output size is more than parameters
    lda #0
    pha
    
    ; push BP, call, then store BP back
    lda 1
    pha
    lda 2
    pha
    jsr irq
    pla
    sta 2
    pla
    sta 1
    
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
    
    .org $fffa
    .word irq_jump_point
    .org $fffc
    .word reset
    .org $fffe
    .word irq_jump_point