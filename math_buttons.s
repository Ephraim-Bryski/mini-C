PORTB = $6000
PORTA = $6001
DDRB = $6002
DDRA = $6003

PCR = $600C
IFR = $600D
IER = $600E


value = $0200 ; 2 bytes
mod10 = $0202 ; 2 bytes
message = $0204 ; 6 bytes
counter = $020a ; 2 bytes

E  = %10000000
RW = %01000000
RS = %00100000

  .org $8000

reset:
  ldx #$ff
  txs
  cli

  lda #%10011011
  sta IER

  ; falling edge interrupt
  lda #$00
  sta PCR


  lda #%11111111 ; Set all pins on port B to output
  sta DDRB
  lda #%11100000 ; Set top 3 pins on port A to output
  sta DDRA

  lda #%00111000 ; Set 8-bit mode; 2-line display; 5x8 font
  jsr lcd_instruction
  lda #%00001110 ; Display on; cursor on; blink off
  jsr lcd_instruction
  lda #%00000110 ; Increment and shift cursor; don't shift display
  jsr lcd_instruction
  lda #%00000001 ; Clear display
  jsr lcd_instruction

  lda #0
  sta counter
  sta counter + 1

  ; jsr update_display

; really should be a subroutine since im using the same code for printing the counter
; but then the message address would have to be a parameter
; and that gets tricky cause it's two bytes
    ldx #0
; print_start_message:
;   lda start_message, x
;   beq loop
;   jsr print_char
;   inx
;   jmp print_start_message


loop:
  jmp loop
  


update_display:

  pha
  txa
  pha
  tya
  pha


  lda #%00000001 ; Clear display

  jsr lcd_instruction

  lda #0
  sta message

  ; Initialize value to be the number to convert
  lda counter
  sta value
  lda counter + 1
  sta value + 1
  
  
divide:
  ; Initialize the remainder to zero
  lda #0
  sta mod10
  sta mod10 + 1
  clc

  ldx #16

divloop:
  ; Rotate quotient and remainder
  rol value
  rol value + 1
  rol mod10
  rol mod10 + 1

  ; a,y = dividend - devisor
  sec
  lda mod10
  sbc #10
  tay ; save low byte in Y
  lda mod10+1
  sbc #0
  bcc ignore_result ; branch if dividend < devisor
  sty mod10
  sta mod10 + 1

ignore_result:
  dex
  bne divloop
  rol value ; shift in the last bit of the quotient
  rol value + 1

  lda mod10
  clc
  adc #"0"
  jsr  push_char

  ; if value != 0, then continue dividing
  lda value
  ora value + 1
  bne divide ; branch if value not equal to 0

  ldx #0
print:
  lda message, x
  beq exit_update_display
  jsr print_char
  inx
  jmp print

exit_update_display:

  pla
  tay
  pla
  tax
  pla


  rts


; start_message:
;   .asciiz "Hello :)"

; Add the character in the A register to the beginning of the 
; null-terminated string `message`
push_char:
  pha ; Push new first char onto stack
  ldy #0

char_loop:
  lda message,y ; Get char on the string and put into X
  tax
  pla
  sta message,y ; Pull char off stack and add it to the string
  iny
  txa
  pha           ; Push char from string onto stack
  bne char_loop

  pla
  sta message,y ; Pull the null off the stack and add to the end of the string

  rts

lcd_wait:
  pha
  lda #%00000000  ; Port B is input
  sta DDRB
lcdbusy:
  lda #RW
  sta PORTA
  lda #(RW | E)
  sta PORTA
  lda PORTB
  and #%10000000
  bne lcdbusy

  lda #RW
  sta PORTA
  lda #%11111111  ; Port B is output
  sta DDRB
  pla
  rts

lcd_instruction:
  jsr lcd_wait
  sta PORTB
  lda #0         ; Clear RS/RW/E bits
  sta PORTA
  lda #E         ; Set E bit to send instruction
  sta PORTA
  lda #0         ; Clear RS/RW/E bits
  sta PORTA
  rts

print_char:
  jsr lcd_wait
  sta PORTB
  lda #RS         ; Set RS; Clear RW/E bits
  sta PORTA
  lda #(RS | E)   ; Set E bit to send instruction
  sta PORTA
  lda #RS         ; Clear E bits
  sta PORTA
  rts

nmi:
irq:

  pha
  txa
  pha
  tya
  pha

  ldy #$ff
  ldx #$ff


delay:
  dex
  bne delay
  dey
  bne delay


  ; bit PORTA



  lda IFR
  cmp #%10001000
  bne skip_rol
  clc
  rol counter  
  rol counter+1
skip_rol:


  lda IFR
  cmp #%10010000
  bne skip_ror  
  clc
  ror counter+1
  ror counter  
skip_ror:


  lda IFR
  cmp #%10000010
  bne skip_increment

  inc counter
  bne exit_irq
  inc counter + 1

skip_increment:

  lda IFR
  cmp #%10000001
  bne skip_decrement

  dec counter
  lda counter
  cmp #255
  bne exit_irq
  dec counter + 1

skip_decrement:
 
  lda #20
  sta counter
  

exit_irq:  

 


  lda #%00011011
  sta IER



  ; update display reads from PORTA signaling interrupt end so needs to be after delay
  jsr update_display


  ; just for reading porta, tells 6522 to clear interrupt flag
  ; not needed now?
  ; bit PORTA



  lda #%10011011
  sta IER

  pla
  tay
  pla
  tax
  pla

  rti

  .org $fffa
  .word nmi
  .word reset
  .word irq