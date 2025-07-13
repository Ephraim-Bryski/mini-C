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
    
    ; store number
    lda #0
    pha
    lda #96
    pha
    
    ; store number
    lda #1
    pha
    lda #96
    pha
    
    ; store number
    lda #2
    pha
    lda #96
    pha
    
    ; store number
    lda #3
    pha
    lda #96
    pha
    
    ; store number
    lda #128
    pha
    
    ; store number
    lda #64
    pha
    
    ; store number
    lda #32
    pha
    
    ; store number
    lda #16
    pha
    
    ; store number
    lda #20
    pha
    
    ; store number
    lda #1
    pha
    
    ; store number
    lda #2
    pha
    
    ; store number
    lda #64
    pha
    
    ; store number
    lda #40
    pha
    
    ; store number
    lda #16
    pha
    jmp initialize_lcd_skip_0
initialize_lcd:
    
; store the stack pointer into the base pointer:
    tsx
    stx 1
    lda #1
    sta 2
    
    ; store number
    lda #255
    pha
    sec
    lda 6
    sbc #5
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    sta 4
    pla
    sta 3
    pla
    ldy #0
    sta (3),Y
    
    ; store number
    lda #224
    pha
    sec
    lda 6
    sbc #7
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    sta 4
    pla
    sta 3
    pla
    ldy #0
    sta (3),Y
    
    ; store number
    lda #56
    pha
    
    ; push BP, call, then store BP back
    lda 1
    pha
    lda 2
    pha
    jsr send_lcd_instruction
    pla
    sta 2
    pla
    sta 1
    pla
    
    ; store number
    lda #14
    pha
    
    ; push BP, call, then store BP back
    lda 1
    pha
    lda 2
    pha
    jsr send_lcd_instruction
    pla
    sta 2
    pla
    sta 1
    pla
    
    ; store number
    lda #6
    pha
    
    ; push BP, call, then store BP back
    lda 1
    pha
    lda 2
    pha
    jsr send_lcd_instruction
    pla
    sta 2
    pla
    sta 1
    pla
    sec
    lda 6
    sbc #13
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    
    ; push BP, call, then store BP back
    lda 1
    pha
    lda 2
    pha
    jsr send_lcd_instruction
    pla
    sta 2
    pla
    sta 1
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
initialize_lcd_skip_0:
    jmp send_lcd_instruction_skip_1
send_lcd_instruction:
    
; store the stack pointer into the base pointer:
    tsx
    stx 1
    lda #1
    sta 2
    
    ; prepare X to the base pointer for pushing parameters to the stack
    lda 1
    sta 3
    lda 2
    sta 4
    ldy #5
    lda (3),Y
    pha
    
    ; fill in placeholders since output size is more than parameters
    lda #0
    pha
    
    ; push BP, call, then store BP back
    lda 1
    pha
    lda 2
    pha
    jsr lcd_wait
    pla
    sta 2
    pla
    sta 1
    pla
    sec
    lda 1
    sbc #0
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    sec
    lda 6
    sbc #1
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    sta 4
    pla
    sta 3
    pla
    ldy #0
    sta (3),Y
    
    ; store number
    lda #0
    pha
    sec
    lda 6
    sbc #3
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    sta 4
    pla
    sta 3
    pla
    ldy #0
    sta (3),Y
    sec
    lda 6
    sbc #8
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    sec
    lda 6
    sbc #3
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    sta 4
    pla
    sta 3
    pla
    ldy #0
    sta (3),Y
    
    ; store number
    lda #0
    pha
    sec
    lda 6
    sbc #3
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    sta 4
    pla
    sta 3
    pla
    ldy #0
    sta (3),Y
    
    ; fill in placeholders since output size is more than parameters
    lda #0
    pha
    
    ; push BP, call, then store BP back
    lda 1
    pha
    lda 2
    pha
    jsr lcd_wait
    pla
    sta 2
    pla
    sta 1
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
send_lcd_instruction_skip_1:
    jmp print_char_skip_2
print_char:
    
; store the stack pointer into the base pointer:
    tsx
    stx 1
    lda #1
    sta 2
    
    ; prepare X to the base pointer for pushing parameters to the stack
    lda 1
    sta 3
    lda 2
    sta 4
    ldy #5
    lda (3),Y
    pha
    
    ; fill in placeholders since output size is more than parameters
    lda #0
    pha
    
    ; push BP, call, then store BP back
    lda 1
    pha
    lda 2
    pha
    jsr lcd_wait
    pla
    sta 2
    pla
    sta 1
    pla
    sec
    lda 1
    sbc #0
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    sec
    lda 6
    sbc #1
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    sta 4
    pla
    sta 3
    pla
    ldy #0
    sta (3),Y
    sec
    lda 6
    sbc #10
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    sec
    lda 6
    sbc #3
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    sta 4
    pla
    sta 3
    pla
    ldy #0
    sta (3),Y
    sec
    lda 6
    sbc #10
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    sec
    lda 6
    sbc #8
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    clc
    tsx
    stx 3
    ldx #1 ; high byte of stack pointer
    stx 4
    ldy #2
    lda (3),Y
    pha
    ldy #1
    lda (3),Y
    sta 5
    pla
    ora 5
    ldy #2
    sta (3),Y
    pla
    sec
    lda 6
    sbc #3
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    sta 4
    pla
    sta 3
    pla
    ldy #0
    sta (3),Y
    sec
    lda 6
    sbc #10
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    sec
    lda 6
    sbc #3
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    sta 4
    pla
    sta 3
    pla
    ldy #0
    sta (3),Y
    
    ; fill in placeholders since output size is more than parameters
    lda #0
    pha
    
    ; push BP, call, then store BP back
    lda 1
    pha
    lda 2
    pha
    jsr lcd_wait
    pla
    sta 2
    pla
    sta 1
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
print_char_skip_2:
    jmp lcd_wait_skip_3
lcd_wait:
    
; store the stack pointer into the base pointer:
    tsx
    stx 1
    lda #1
    sta 2
    
    ; store number
    lda #0
    pha
    sec
    lda 6
    sbc #5
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    sta 4
    pla
    sta 3
    pla
    ldy #0
    sta (3),Y
    
    ; store number
    lda #1
    pha
while_loop_5:
    sec
    lda 1
    sbc #0
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    pla
    cmp #0
    beq branch_selected_8
    jmp jump_skip_7
branch_selected_8:
    jmp while_exit_6
jump_skip_7:
    sec
    lda 6
    sbc #9
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    sec
    lda 6
    sbc #3
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    sta 4
    pla
    sta 3
    pla
    ldy #0
    sta (3),Y
    sec
    lda 6
    sbc #9
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    sec
    lda 6
    sbc #8
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    clc
    tsx
    stx 3
    ldx #1 ; high byte of stack pointer
    stx 4
    ldy #2
    lda (3),Y
    pha
    ldy #1
    lda (3),Y
    sta 5
    pla
    ora 5
    ldy #2
    sta (3),Y
    pla
    sec
    lda 6
    sbc #3
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    sta 4
    pla
    sta 3
    pla
    ldy #0
    sta (3),Y
    sec
    lda 6
    sbc #1
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    sta 4
    pla
    sta 3
    ldy #0
    lda (3),Y
    pha
    
    ; store number
    lda #128
    pha
    clc
    tsx
    stx 3
    ldx #1 ; high byte of stack pointer
    stx 4
    ldy #2
    lda (3),Y
    pha
    ldy #1
    lda (3),Y
    sta 5
    pla
    and 5
    ldy #2
    sta (3),Y
    pla
    sec
    lda 1
    sbc #0
    sta 3
    lda 2
    sbc #0
    sta 4
    pla
    ldy #0
    sta (3),Y
while_continue_4:
    sec
    lda 1
    sbc #1
    tax
    txs
    jmp while_loop_5
while_exit_6:
    sec
    lda 1
    sbc #1
    tax
    txs
    sec
    lda 6
    sbc #9
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    sec
    lda 6
    sbc #3
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    sta 4
    pla
    sta 3
    pla
    ldy #0
    sta (3),Y
    
    ; store number
    lda #255
    pha
    sec
    lda 6
    sbc #5
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    sta 4
    pla
    sta 3
    pla
    ldy #0
    sta (3),Y
    
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
lcd_wait_skip_3:
    jmp switch_line_skip_9
switch_line:
    
; store the stack pointer into the base pointer:
    tsx
    stx 1
    lda #1
    sta 2
    
    ; defaulting uninitialized i to 0
    lda #0
    pha
    
    ; store number
    lda #0
    pha
    sec
    lda 1
    sbc #0
    sta 3
    lda 2
    sbc #0
    sta 4
    pla
    ldy #0
    sta (3),Y
for_loop_10:
    sec
    lda 1
    sbc #0
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    sec
    lda 6
    sbc #16
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    sec
    tsx
    stx 3
    ldx #1 ; high byte of stack pointer
    stx 4
    ldy #2
    lda (3),Y
    pha
    ldy #1
    lda (3),Y
    sta 5
    pla
    sbc 5
    ldy #2
    sta (3),Y
    pla
    pla
    lda #1
    bcc branch_selected_15
    jmp jump_skip_14
branch_selected_15:
    jmp greater_true_13
jump_skip_14:
    lda #0
greater_true_13:
    pha
    pla
    cmp #0
    beq branch_selected_17
    jmp jump_skip_16
branch_selected_17:
    jmp for_exit_12
jump_skip_16:
    sec
    lda 6
    sbc #12
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    
    ; push BP, call, then store BP back
    lda 1
    pha
    lda 2
    pha
    jsr send_lcd_instruction
    pla
    sta 2
    pla
    sta 1
    pla
continue_loop_11:
    sec
    lda 1
    sbc #1
    tax
    txs
    sec
    lda 1
    sbc #0
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    
    ; store number
    lda #1
    pha
    clc
    tsx
    stx 3
    ldx #1 ; high byte of stack pointer
    stx 4
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
    sec
    lda 1
    sbc #0
    sta 3
    lda 2
    sbc #0
    sta 4
    pla
    ldy #0
    sta (3),Y
    jmp for_loop_10
for_exit_12:
    sec
    lda 1
    sbc #1
    tax
    txs
    
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
switch_line_skip_9:
    jmp get_address_counter_skip_18
get_address_counter:
    
; store the stack pointer into the base pointer:
    tsx
    stx 1
    lda #1
    sta 2
    
    ; store number
    lda #0
    pha
    sec
    lda 6
    sbc #5
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    sta 4
    pla
    sta 3
    pla
    ldy #0
    sta (3),Y
    sec
    lda 6
    sbc #9
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    sec
    lda 6
    sbc #3
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    sta 4
    pla
    sta 3
    pla
    ldy #0
    sta (3),Y
    sec
    lda 6
    sbc #9
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    sec
    lda 6
    sbc #8
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    clc
    tsx
    stx 3
    ldx #1 ; high byte of stack pointer
    stx 4
    ldy #2
    lda (3),Y
    pha
    ldy #1
    lda (3),Y
    sta 5
    pla
    ora 5
    ldy #2
    sta (3),Y
    pla
    sec
    lda 6
    sbc #3
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    sta 4
    pla
    sta 3
    pla
    ldy #0
    sta (3),Y
    sec
    lda 6
    sbc #1
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    sta 4
    pla
    sta 3
    ldy #0
    lda (3),Y
    pha
    
    ; store number
    lda #127
    pha
    clc
    tsx
    stx 3
    ldx #1 ; high byte of stack pointer
    stx 4
    ldy #2
    lda (3),Y
    pha
    ldy #1
    lda (3),Y
    sta 5
    pla
    and 5
    ldy #2
    sta (3),Y
    pla
    sec
    lda 6
    sbc #9
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    sec
    lda 6
    sbc #3
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    sta 4
    pla
    sta 3
    pla
    ldy #0
    sta (3),Y
    
    ; store number
    lda #255
    pha
    sec
    lda 6
    sbc #5
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    sta 4
    pla
    sta 3
    pla
    ldy #0
    sta (3),Y
    sec
    lda 1
    sbc #0
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
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
get_address_counter_skip_18:
    jmp get_cursor_char_idx_skip_19
get_cursor_char_idx:
    
; store the stack pointer into the base pointer:
    tsx
    stx 1
    lda #1
    sta 2
    
    ; fill in placeholders since output size is more than parameters
    lda #0
    pha
    
    ; push BP, call, then store BP back
    lda 1
    pha
    lda 2
    pha
    jsr lcd_wait
    pla
    sta 2
    pla
    sta 1
    pla
    
    ; fill in placeholders since output size is more than parameters
    lda #0
    pha
    
    ; push BP, call, then store BP back
    lda 1
    pha
    lda 2
    pha
    jsr get_address_counter
    pla
    sta 2
    pla
    sta 1
    sec
    lda 1
    sbc #0
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    sec
    lda 6
    sbc #15
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    sec
    tsx
    stx 3
    ldx #1 ; high byte of stack pointer
    stx 4
    ldy #2
    lda (3),Y
    pha
    ldy #1
    lda (3),Y
    sta 5
    pla
    sbc 5
    ldy #2
    sta (3),Y
    pla
    pla
    lda #1
    bcs branch_selected_24
    jmp jump_skip_23
branch_selected_24:
    jmp greater_true_22
jump_skip_23:
    lda #0
greater_true_22:
    pha
    pla
    cmp #0
    beq branch_selected_26
    jmp jump_skip_25
branch_selected_26:
    jmp if_skip_21
jump_skip_25:
    sec
    lda 1
    sbc #0
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    sec
    lda 6
    sbc #15
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    sec
    tsx
    stx 3
    ldx #1 ; high byte of stack pointer
    stx 4
    ldy #2
    lda (3),Y
    pha
    ldy #1
    lda (3),Y
    sta 5
    pla
    sbc 5
    ldy #2
    sta (3),Y
    pla
    
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
    jmp if_end_20
if_skip_21:
    
    ; store number
    lda #1
    pha
    pla
    cmp #0
    beq branch_selected_29
    jmp jump_skip_28
branch_selected_29:
    jmp if_skip_27
jump_skip_28:
    sec
    lda 1
    sbc #0
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
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
    jmp if_end_20
if_skip_27:
if_end_20:
    sec
    lda 1
    sbc #1
    tax
    txs
    
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
get_cursor_char_idx_skip_19:
    jmp get_cursor_line_idx_skip_30
get_cursor_line_idx:
    
; store the stack pointer into the base pointer:
    tsx
    stx 1
    lda #1
    sta 2
    
    ; fill in placeholders since output size is more than parameters
    lda #0
    pha
    
    ; push BP, call, then store BP back
    lda 1
    pha
    lda 2
    pha
    jsr lcd_wait
    pla
    sta 2
    pla
    sta 1
    pla
    
    ; fill in placeholders since output size is more than parameters
    lda #0
    pha
    
    ; push BP, call, then store BP back
    lda 1
    pha
    lda 2
    pha
    jsr get_address_counter
    pla
    sta 2
    pla
    sta 1
    sec
    lda 1
    sbc #0
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    sec
    lda 6
    sbc #15
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    sec
    tsx
    stx 3
    ldx #1 ; high byte of stack pointer
    stx 4
    ldy #2
    lda (3),Y
    pha
    ldy #1
    lda (3),Y
    sta 5
    pla
    sbc 5
    ldy #2
    sta (3),Y
    pla
    pla
    lda #1
    bcs branch_selected_35
    jmp jump_skip_34
branch_selected_35:
    jmp greater_true_33
jump_skip_34:
    lda #0
greater_true_33:
    pha
    pla
    cmp #0
    beq branch_selected_37
    jmp jump_skip_36
branch_selected_37:
    jmp if_skip_32
jump_skip_36:
    
    ; store number
    lda #1
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
    jmp if_end_31
if_skip_32:
    
    ; store number
    lda #1
    pha
    pla
    cmp #0
    beq branch_selected_40
    jmp jump_skip_39
branch_selected_40:
    jmp if_skip_38
jump_skip_39:
    
    ; store number
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
    jmp if_end_31
if_skip_38:
if_end_31:
    sec
    lda 1
    sbc #1
    tax
    txs
    
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
get_cursor_line_idx_skip_30:
    jmp set_cursor_skip_41
set_cursor:
    
; store the stack pointer into the base pointer:
    tsx
    stx 1
    lda #1
    sta 2
    
    ; prepare X to the base pointer for pushing parameters to the stack
    lda 1
    sta 3
    lda 2
    sta 4
    ldy #6
    lda (3),Y
    pha
    ldy #5
    lda (3),Y
    pha
    sec
    lda 1
    sbc #0
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    
    ; store number
    lda #64
    pha
    pla
    tax
    pla
    sta 5
    lda #0
    clc
multiply_loop_42:
    adc 5
    dex
    bne multiply_loop_42
    pha
    lda #0; FUTURE right now im assuming the product is only 1 byte
    pha
    sec
    lda 1
    sbc #1
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    clc
    tsx
    stx 3
    ldx #1 ; high byte of stack pointer
    stx 4
    ldy #3
    lda (3),Y
    pha
    ldy #1
    lda (3),Y
    sta 5
    pla
    adc 5
    ldy #3
    sta (3),Y
    ldy #2
    lda (3),Y
    ldx #0
    stx 5
    adc 5
    ldy #2
    sta (3),Y
    pla
    pla
    sec
    lda 1
    sbc #2
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    
    ; store number
    lda #128
    pha
    clc
    tsx
    stx 3
    ldx #1 ; high byte of stack pointer
    stx 4
    ldy #2
    lda (3),Y
    pha
    ldy #1
    lda (3),Y
    sta 5
    pla
    ora 5
    ldy #2
    sta (3),Y
    pla
    
    ; push BP, call, then store BP back
    lda 1
    pha
    lda 2
    pha
    jsr send_lcd_instruction
    pla
    sta 2
    pla
    sta 1
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
set_cursor_skip_41:
    jmp str_length_skip_43
str_length:
    
; store the stack pointer into the base pointer:
    tsx
    stx 1
    lda #1
    sta 2
    
    ; prepare X to the base pointer for pushing parameters to the stack
    lda 1
    sta 3
    lda 2
    sta 4
    ldy #6
    lda (3),Y
    pha
    ldy #5
    lda (3),Y
    pha
    
    ; store number
    lda #0
    pha
    lda #0
    pha
while_loop_45:
    
    ; store number
    lda #1
    pha
    pla
    cmp #0
    beq branch_selected_48
    jmp jump_skip_47
branch_selected_48:
    jmp while_exit_46
jump_skip_47:
    sec
    lda 1
    sbc #1
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    sec
    lda 1
    sbc #3
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    
    ; store number
    lda #1
    pha
    pla
    tax
    pla
    sta 5
    lda #0
    clc
multiply_loop_49:
    adc 5
    dex
    bne multiply_loop_49
    pha
    lda #0; FUTURE right now im assuming the product is only 1 byte
    pha
    clc
    tsx
    stx 3
    ldx #1 ; high byte of stack pointer
    stx 4
    ldy #4
    lda (3),Y
    pha
    ldy #2
    lda (3),Y
    sta 5
    pla
    adc 5
    ldy #4
    sta (3),Y
    ldy #3
    lda (3),Y
    pha
    ldy #1
    lda (3),Y
    sta 5
    pla
    adc 5
    ldy #3
    sta (3),Y
    pla
    pla
    pla
    sta 4
    pla
    sta 3
    ldy #0
    lda (3),Y
    pha
    sec
    lda 1
    sbc #4
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    
    ; store number
    lda #0
    pha
    clc
    tsx
    stx 3
    ldx #1 ; high byte of stack pointer
    stx 4
    ldy #2
    lda (3),Y
    pha
    ldy #1
    lda (3),Y
    sta 5
    pla
    cmp 5
    bne branch_selected_55
    jmp jump_skip_54
branch_selected_55:
    jmp equal_false_52
jump_skip_54:
    lda #1
    jmp equal_exit_53
equal_false_52:
    lda #0
equal_exit_53:
    ldy #2
    sta (3),Y
    pla
    pla
    cmp #0
    beq branch_selected_57
    jmp jump_skip_56
branch_selected_57:
    jmp if_skip_51
jump_skip_56:
    sec
    lda 1
    sbc #3
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
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
    sta 3
    lda 2
    sta 4
    pla
    ldy #6
    sta (3),Y
    lda 1
    tax
    txs
    rts
    jmp if_end_50
if_skip_51:
if_end_50:
    sec
    lda 1
    sbc #5
    tax
    txs
    sec
    lda 1
    sbc #3
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    
    ; store number
    lda #1
    pha
    clc
    tsx
    stx 3
    ldx #1 ; high byte of stack pointer
    stx 4
    ldy #3
    lda (3),Y
    pha
    ldy #1
    lda (3),Y
    sta 5
    pla
    adc 5
    ldy #3
    sta (3),Y
    ldy #2
    lda (3),Y
    ldx #0
    stx 5
    adc 5
    ldy #2
    sta (3),Y
    pla
    sec
    lda 1
    sbc #3
    sta 3
    lda 2
    sbc #0
    sta 4
    pla
    ldy #0
    sta (3),Y
    pla
    ldy #1
    sta (3),Y
while_continue_44:
    sec
    lda 1
    sbc #4
    tax
    txs
    jmp while_loop_45
while_exit_46:
    sec
    lda 1
    sbc #4
    tax
    txs
    
    ; default return value of 0
    lda #0
    pha
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
    sta 3
    lda 2
    sta 4
    pla
    ldy #6
    sta (3),Y
    lda 1
    tax
    txs
    rts
str_length_skip_43:
    jmp print_newline_skip_58
print_newline:
    
; store the stack pointer into the base pointer:
    tsx
    stx 1
    lda #1
    sta 2
    
    ; store number
    lda #10
    pha
    
    ; push BP, call, then store BP back
    lda 1
    pha
    lda 2
    pha
    jsr print_char
    pla
    sta 2
    pla
    sta 1
    pla
    
    ; default return value of 0
    lda #0
    pha
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
    sta 3
    lda 2
    sta 4
    pla
    ldy #6
    sta (3),Y
    lda 1
    tax
    txs
    rts
print_newline_skip_58:
    jmp print_string_skip_59
print_string:
    
; store the stack pointer into the base pointer:
    tsx
    stx 1
    lda #1
    sta 2
    
    ; prepare X to the base pointer for pushing parameters to the stack
    lda 1
    sta 3
    lda 2
    sta 4
    ldy #6
    lda (3),Y
    pha
    ldy #5
    lda (3),Y
    pha
    sec
    lda 1
    sbc #1
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    
    ; push BP, call, then store BP back
    lda 1
    pha
    lda 2
    pha
    jsr str_length
    pla
    sta 2
    pla
    sta 1
    
    ; store number
    lda #0
    pha
    lda #0
    pha
    
    ; store number
    lda #0
    pha
    lda #0
    pha
    sec
    lda 1
    sbc #5
    sta 3
    lda 2
    sbc #0
    sta 4
    pla
    ldy #0
    sta (3),Y
    pla
    ldy #1
    sta (3),Y
for_loop_60:
    sec
    lda 1
    sbc #5
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    sec
    lda 1
    sbc #3
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    sec
    tsx
    stx 3
    ldx #1 ; high byte of stack pointer
    stx 4
    ldy #4
    lda (3),Y
    pha
    ldy #2
    lda (3),Y
    sta 5
    pla
    sbc 5
    ldy #4
    sta (3),Y
    ldy #3
    lda (3),Y
    pha
    ldy #1
    lda (3),Y
    sta 5
    pla
    sbc 5
    ldy #3
    sta (3),Y
    pla
    pla
    pla
    pla
    lda #1
    bcc branch_selected_65
    jmp jump_skip_64
branch_selected_65:
    jmp greater_true_63
jump_skip_64:
    lda #0
greater_true_63:
    pha
    pla
    cmp #0
    beq branch_selected_67
    jmp jump_skip_66
branch_selected_67:
    jmp for_exit_62
jump_skip_66:
    sec
    lda 1
    sbc #1
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    sec
    lda 1
    sbc #5
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    
    ; store number
    lda #1
    pha
    pla
    tax
    pla
    sta 5
    lda #0
    clc
multiply_loop_68:
    adc 5
    dex
    bne multiply_loop_68
    pha
    lda #0; FUTURE right now im assuming the product is only 1 byte
    pha
    clc
    tsx
    stx 3
    ldx #1 ; high byte of stack pointer
    stx 4
    ldy #4
    lda (3),Y
    pha
    ldy #2
    lda (3),Y
    sta 5
    pla
    adc 5
    ldy #4
    sta (3),Y
    ldy #3
    lda (3),Y
    pha
    ldy #1
    lda (3),Y
    sta 5
    pla
    adc 5
    ldy #3
    sta (3),Y
    pla
    pla
    pla
    sta 4
    pla
    sta 3
    ldy #0
    lda (3),Y
    pha
    
    ; push BP, call, then store BP back
    lda 1
    pha
    lda 2
    pha
    jsr print_char
    pla
    sta 2
    pla
    sta 1
    pla
continue_loop_61:
    sec
    lda 1
    sbc #6
    tax
    txs
    sec
    lda 1
    sbc #5
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    
    ; store number
    lda #1
    pha
    clc
    tsx
    stx 3
    ldx #1 ; high byte of stack pointer
    stx 4
    ldy #3
    lda (3),Y
    pha
    ldy #1
    lda (3),Y
    sta 5
    pla
    adc 5
    ldy #3
    sta (3),Y
    ldy #2
    lda (3),Y
    ldx #0
    stx 5
    adc 5
    ldy #2
    sta (3),Y
    pla
    sec
    lda 1
    sbc #5
    sta 3
    lda 2
    sbc #0
    sta 4
    pla
    ldy #0
    sta (3),Y
    pla
    ldy #1
    sta (3),Y
    jmp for_loop_60
for_exit_62:
    sec
    lda 1
    sbc #6
    tax
    txs
    
    ; default return value of 0
    lda #0
    pha
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
    sta 3
    lda 2
    sta 4
    pla
    ldy #6
    sta (3),Y
    lda 1
    tax
    txs
    rts
print_string_skip_59:
    jmp error_skip_69
error:
    
; store the stack pointer into the base pointer:
    tsx
    stx 1
    lda #1
    sta 2
    
    ; prepare X to the base pointer for pushing parameters to the stack
    lda 1
    sta 3
    lda 2
    sta 4
    ldy #6
    lda (3),Y
    pha
    ldy #5
    lda (3),Y
    pha
    
    ; generating string assembly
    lda #0
    pha
    lda #32
    pha
    lda #58
    pha
    lda #82
    pha
    lda #79
    pha
    lda #82
    pha
    lda #82
    pha
    lda #69
    pha
    tsx
    txa
    clc
    adc #1
    pha
    lda #1
    pha
    sec
    lda 1
    sbc #11
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    
    ; push BP, call, then store BP back
    lda 1
    pha
    lda 2
    pha
    jsr print_string
    pla
    sta 2
    pla
    sta 1
    pla
    pla
    sec
    lda 1
    sbc #1
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    
    ; push BP, call, then store BP back
    lda 1
    pha
    lda 2
    pha
    jsr print_string
    pla
    sta 2
    pla
    sta 1
    pla
    pla
    jmp halt_point
    pla
    
    ; default return value of 0
    lda #0
    pha
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
    sta 3
    lda 2
    sta 4
    pla
    ldy #6
    sta (3),Y
    lda 1
    tax
    txs
    rts
error_skip_69:
    
    ; store number
    lda #13
    pha
    lda #96
    pha
    
    ; store number
    lda #14
    pha
    lda #96
    pha
    
    ; store number
    lda #129
    pha
    
    ; store number
    lda #130
    pha
    
    ; store number
    lda #144
    pha
    
    ; store number
    lda #136
    pha
    jmp main_skip_70
main:
    
; store the stack pointer into the base pointer:
    tsx
    stx 1
    lda #1
    sta 2
    
    ; fill in placeholders since output size is more than parameters
    lda #0
    pha
    
    ; push BP, call, then store BP back
    lda 1
    pha
    lda 2
    pha
    jsr initialize_lcd
    pla
    sta 2
    pla
    sta 1
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
main_skip_70:
    
    ; store number
    lda #16
    pha
    jmp sleep_skip_71
sleep:
    
; store the stack pointer into the base pointer:
    tsx
    stx 1
    lda #1
    sta 2
    
    ; prepare X to the base pointer for pushing parameters to the stack
    lda 1
    sta 3
    lda 2
    sta 4
    ldy #5
    lda (3),Y
    pha
    
    ; store number
    lda #0
    pha
while_loop_73:
    sec
    lda 1
    sbc #1
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    sec
    lda 1
    sbc #0
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    sec
    tsx
    stx 3
    ldx #1 ; high byte of stack pointer
    stx 4
    ldy #2
    lda (3),Y
    pha
    ldy #1
    lda (3),Y
    sta 5
    pla
    sbc 5
    ldy #2
    sta (3),Y
    pla
    pla
    lda #1
    bcc branch_selected_77
    jmp jump_skip_76
branch_selected_77:
    jmp greater_true_75
jump_skip_76:
    lda #0
greater_true_75:
    pha
    pla
    cmp #0
    beq branch_selected_79
    jmp jump_skip_78
branch_selected_79:
    jmp while_exit_74
jump_skip_78:
    
    ; store number
    lda #0
    pha
while_loop_81:
    sec
    lda 1
    sbc #2
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    
    ; store number
    lda #255
    pha
    sec
    tsx
    stx 3
    ldx #1 ; high byte of stack pointer
    stx 4
    ldy #2
    lda (3),Y
    pha
    ldy #1
    lda (3),Y
    sta 5
    pla
    sbc 5
    ldy #2
    sta (3),Y
    pla
    pla
    lda #1
    bcc branch_selected_85
    jmp jump_skip_84
branch_selected_85:
    jmp greater_true_83
jump_skip_84:
    lda #0
greater_true_83:
    pha
    pla
    cmp #0
    beq branch_selected_87
    jmp jump_skip_86
branch_selected_87:
    jmp while_exit_82
jump_skip_86:
    sec
    lda 1
    sbc #2
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    
    ; store number
    lda #1
    pha
    clc
    tsx
    stx 3
    ldx #1 ; high byte of stack pointer
    stx 4
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
    sec
    lda 1
    sbc #2
    sta 3
    lda 2
    sbc #0
    sta 4
    pla
    ldy #0
    sta (3),Y
while_continue_80:
    sec
    lda 1
    sbc #3
    tax
    txs
    jmp while_loop_81
while_exit_82:
    sec
    lda 1
    sbc #3
    tax
    txs
    sec
    lda 1
    sbc #1
    sta 3
    lda 2
    sbc #0
    sta 4
    ldy #0
    lda (3),Y
    pha
    
    ; store number
    lda #1
    pha
    clc
    tsx
    stx 3
    ldx #1 ; high byte of stack pointer
    stx 4
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
    sec
    lda 1
    sbc #1
    sta 3
    lda 2
    sbc #0
    sta 4
    pla
    ldy #0
    sta (3),Y
while_continue_72:
    sec
    lda 1
    sbc #2
    tax
    txs
    jmp while_loop_73
while_exit_74:
    sec
    lda 1
    sbc #2
    tax
    txs
    
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
sleep_skip_71:
    jmp block_interrupts_skip_88
block_interrupts:
    
; store the stack pointer into the base pointer:
    tsx
    stx 1
    lda #1
    sta 2
    
    ; store number
    lda #27
    pha
    sec
    lda 6
    sbc #21
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    sta 4
    pla
    sta 3
    pla
    ldy #0
    sta (3),Y
    
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
block_interrupts_skip_88:
    jmp enable_interrupts_skip_89
enable_interrupts:
    
; store the stack pointer into the base pointer:
    tsx
    stx 1
    lda #1
    sta 2
    
    ; store number
    lda #155
    pha
    sec
    lda 6
    sbc #21
    sta 3
    lda 7
    sbc #0
    sta 4
    ldy #1
    lda (3),Y
    pha
    ldy #0
    lda (3),Y
    pha
    pla
    sta 4
    pla
    sta 3
    pla
    ldy #0
    sta (3),Y
    
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
enable_interrupts_skip_89:
    
    ; store value 97
    lda #97
    pha
    
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

;   ldy #$ff
;   ldx #$ff
; delay:
;   dex
;   bne delay
;   dey
;   bne delay

  ; lda #%00011011
  ; sta IER



  lda IFR
  cmp #%10001000
  bne skip_inc


skip_inc:


  lda IFR
  cmp #%10000001
  
  bne skip_print

    lda #"g"
  jsr print_char
  lda #0
  

skip_print:
  ; just for reading porta, tells 6522 to clear interrupt flag
  ; not needed now?



  bit  $6001
  bit  $6000
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