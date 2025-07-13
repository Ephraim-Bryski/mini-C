; absolute minimal code to compare with compiler output

PORTB = $6000
PORTA = $6001
DDRB = $6002
DDRA = $6003

PCR = $600C
IFR = $600D
IER = $600E

counter = $020a

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

loop:
  jmp loop
  


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
  ; cmp #%10001000
  ; bne skip_inc

  inc counter
  lda counter
  cmp #11
  bne skip_print

skip_inc:

  lda #"x"
  jsr print_char
  lda #0
  sta counter

skip_print:
  ; just for reading porta, tells 6522 to clear interrupt flag
  ; not needed now?



  bit PORTA
  bit PORTB
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