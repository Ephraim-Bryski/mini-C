PCR = $600C
IFR = $600D
IER = $600E
BASE_P_LOW = 1
BASE_P_HIGH = 2
GLOBAL_P_LOW = 3
GLOBAL_P_HIGH = 4
LOW_INDIRECT_BP = 5
HIGH_INDIRECT_BP = 6
LOW_INDIRECT_GP = 7
HIGH_INDIRECT_GP = 8
LOW_INDIRECT_ARRAY = 9
HIGH_INDIRECT_ARRAY = 10
RIGHT_SIDE = 11
    .org $8000
reset:
    cld
    cli
    lda #%10011011 ; allow via to handle interrupts
    sta IER
    ldx #$ff
    txs
; the high base pointer will always be 1:
    lda #1
    sta BASE_P_HIGH
    ; falling edge interrupt
    lda #$00
    sta PCR
    tsx
    stx GLOBAL_P_LOW
    lda #1
    sta GLOBAL_P_HIGH
; prepare indirect memory offset:
    sec
    lda GLOBAL_P_LOW
    sbc #200
    sta LOW_INDIRECT_GP
    lda GLOBAL_P_HIGH
    sbc #0
    sta HIGH_INDIRECT_GP
    
; get declaration:
    ; store number
    lda #4
    pha
    jmp main_skip_0
main:
    
; store the stack pointer into the base pointer:
    sec
    tsx
    stx BASE_P_LOW
    txa
    sbc #200
    sta LOW_INDIRECT_BP
    lda #1
    sbc #0
    sta HIGH_INDIRECT_BP
    
; retrieve variable:
; load indirect:
    ; OFFSET_TEST
    ldy #200
    lda (LOW_INDIRECT_GP),Y
; push variable on stack:
    pha
; pop unused expression ouput:
    pla
    
    ; default return value of 0
    lda #0
    pha
    
; store output bytes back where it can be retrieved by the caller:
    pla
    ; store byte
    ; OFFSET_TEST
    ldy #5
    sta (BASE_P_LOW),Y
    ldx BASE_P_LOW
    txs
    rts
main_skip_0:
    jmp irq_skip_1
irq:
    
; store the stack pointer into the base pointer:
    sec
    tsx
    stx BASE_P_LOW
    txa
    sbc #200
    sta LOW_INDIRECT_BP
    lda #1
    sbc #0
    sta HIGH_INDIRECT_BP
    
    ; default return value of 0
    lda #0
    pha
    
; store output bytes back where it can be retrieved by the caller:
    pla
    ; store byte
    ; OFFSET_TEST
    ldy #5
    sta (BASE_P_LOW),Y
    ldx BASE_P_LOW
    txs
    rts
irq_skip_1:
    
    ; fill in placeholders since output size is more than parameters
    lda #0
    pha
    
    ; push BP, call, then store BP back
    lda BASE_P_LOW
    pha
    lda BASE_P_HIGH
    pha
    jsr main
    sec
    pla
    tax
    pla
    sta BASE_P_LOW
    sbc #200
    sta LOW_INDIRECT_BP
    txa
    sbc #0
    sta HIGH_INDIRECT_BP
    tsx
; load from stack pointer:
    lda (257),X
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
    lda BASE_P_LOW
    pha
    lda BASE_P_HIGH
    pha
    jsr irq
    sec
    pla
    tax
    pla
    sta BASE_P_LOW
    sbc #200
    sta LOW_INDIRECT_BP
    txa
    sbc #0
    sta HIGH_INDIRECT_BP
    
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