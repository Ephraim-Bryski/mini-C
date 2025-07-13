
char* PORTB = (char*) 0x6000;
char* PORTA = (char*) 0x6001;
char* DDRB = (char*) 0x6002;
char* DDRA = (char*) 0x6003;

char E =  0b10000000;
char RW = 0b01000000;
char RS = 0b00100000;

char LCD_SHIFT_LEFT =   0b00010000;
char LCD_SHIFT_RIGHT =  0b00010100;
char LCD_CLEAR =        0b00000001;
char LCD_RETURN_HOME =  0b00000010;

char ADDRESS_LINE_JUMP = 64;
char N_CHARS_PER_LINE = 40;
char N_VISIBLE_CHARS_PER_LINE = 16;



char initialize_lcd(){
    // set lcd display lines (blue) to all be output
    DDRB[0] = 0b11111111;
    // set lcd info lines (yellow) to all be output
    DDRA[0] = 0b11100000;

    
    // sets two line display
    send_lcd_instruction(0b00111000);
    // turns display on
    send_lcd_instruction(0b00001110);
    // sets to increment cursor mode
    send_lcd_instruction(0b00000110);
    // clearing anyway puts ddram back to 0
    send_lcd_instruction(LCD_CLEAR);
}

char send_lcd_instruction(char value){
    lcd_wait();
    PORTB[0] = value;
    PORTA[0] = 0;
    PORTA[0] = E;
    PORTA[0] = 0;
    lcd_wait();
}

char print_char(char value){
    lcd_wait();
    PORTB[0] = value;
    PORTA[0] = RS;
    PORTA[0] = RS|E;
    PORTA[0] = RS;
    lcd_wait();
}

char lcd_wait(){
    DDRB[0] = 0;
    char busy = 1;
    while(busy){
        PORTA[0] = RW;
        PORTA[0] = RW|E;
        busy = PORTB[0] & 0b10000000;
    }
    PORTA[0] = RW;
    DDRB[0] = 0b11111111;
}




char switch_line(){
    char i;
    for (i=0;i<N_CHARS_PER_LINE;i=i+1){
        send_lcd_instruction(LCD_SHIFT_RIGHT);
    }
}



char get_address_counter(){
    DDRB[0] = 0;
    
    PORTA[0] = RW;
    PORTA[0] = RW|E;
    char address = PORTB[0] & 0b01111111;
    PORTA[0] = RW;
    DDRB[0] = 0b11111111;
    return address;
}



char get_cursor_char_idx(){
    lcd_wait();
    char address = get_address_counter();
    if (address >= ADDRESS_LINE_JUMP){
        return address - ADDRESS_LINE_JUMP;
    }else{
        return address;
    }
}

char get_cursor_line_idx(){
    lcd_wait();
    char address = get_address_counter();
    if (address >= ADDRESS_LINE_JUMP){
        return 1;
    }else{
        return 0;
    }
}





char set_cursor(char line_idx, char char_idx){
    char address = line_idx * 64 + char_idx;
    send_lcd_instruction(address | 0b10000000);
}   

