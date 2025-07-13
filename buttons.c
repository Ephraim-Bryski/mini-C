
#include "lib/lcd.c"
#include "lib/strings.c"

char* IFR = (char*) 0x600D;
char* IER = (char*) 0x600E;

char BUTTON_1 = 0b10000001;
char BUTTON_2 = 0b10000010;
char BUTTON_3 = 0b10010000;
char BUTTON_4 = 0b10001000;

char sleep(char n){
    // bigger n means longer sleep
    // of course changing the compiler implementation can change the sleep time
    char i = 0;
    while (i<n){
        char j = 0;
        while (j<255){
            j = j+1;
        }
        i = i+1;
    }
}

char GUY_CHAR = 'G';
char GUY_CHAR_PER_LINE_IDX = 10;
char guy_line_idx = 0;

char bullet_char_per_line_idx = 0;
char bullet_line_idx = 0;


char LEFT = 0;
char RIGHT = 1;
char VERTICAL = 2;


char main(){
    initialize_lcd();
    move_guy(RIGHT);
    while (1){



        print_char(' ');
        print_char('>');
        send_lcd_instruction(LCD_SHIFT_LEFT);
        sleep(3);
        
        bullet_char_per_line_idx += 1;
        check_hit();
        if (bullet_char_per_line_idx == N_VISIBLE_CHARS_PER_LINE+1){
            bullet_line_idx = !bullet_line_idx;
            bullet_char_per_line_idx = 0;
            

            set_cursor(bullet_line_idx, bullet_char_per_line_idx);
        }
        // sleep(1);
    }
    // print_char('H');
}

char block_interrupts(){
    IER[0] = 0b00011011;
    // TODO not sure why this is needed
    // otherwise nothing prints after exiting interrupt
    lcd_wait();
}
char enable_interrupts(){
    IER[0] = 0b10011011;
}


char check_hit(){
    if (bullet_char_per_line_idx == GUY_CHAR_PER_LINE_IDX && bullet_line_idx == guy_line_idx ){
        send_lcd_instruction(LCD_CLEAR);
        send_lcd_instruction(LCD_RETURN_HOME);
        print_string("You lose :(");
        while (1){}
    }

}

char move_guy(char direction){

    char move_code;
    char reverse_move_code;
    char move_amount;

    
    char original_char_idx = get_cursor_char_idx();
    char original_line_idx = get_cursor_line_idx();
    
    char new_char_per_line_idx;
    char new_line_idx;
    if (direction == LEFT && GUY_CHAR_PER_LINE_IDX > 0){
        new_char_per_line_idx = GUY_CHAR_PER_LINE_IDX - 1;
        new_line_idx = guy_line_idx;
    }
    else if (direction == RIGHT && GUY_CHAR_PER_LINE_IDX < N_VISIBLE_CHARS_PER_LINE){
        new_char_per_line_idx = GUY_CHAR_PER_LINE_IDX + 1;
        new_line_idx = guy_line_idx;
    }
    else if (direction == VERTICAL){
        new_char_per_line_idx = GUY_CHAR_PER_LINE_IDX;
        new_line_idx = !guy_line_idx;
    }
    else {
        // would happen if a wall is hit on the left or right
        new_char_per_line_idx = GUY_CHAR_PER_LINE_IDX;
        new_line_idx = guy_line_idx;
    }
    
    set_cursor(guy_line_idx, GUY_CHAR_PER_LINE_IDX);
    print_char(' ');
    set_cursor(new_line_idx, new_char_per_line_idx);
    print_char(GUY_CHAR);
    set_cursor(original_line_idx, original_char_idx);

    guy_line_idx = new_line_idx;
    GUY_CHAR_PER_LINE_IDX = new_char_per_line_idx;

    check_hit();
}

char irq(){
    char irq_flag = IFR[0];
    block_interrupts();

    if (irq_flag == BUTTON_1){
        move_guy(LEFT);
    }else if (irq_flag == BUTTON_2){
        move_guy(VERTICAL);
    }else if (irq_flag == BUTTON_3){
        move_guy(RIGHT);
    }

    // if (irq_flag == BUTTON_1){
    //     send_lcd_instruction(LCD_RETURN_HOME);
    // }else {
    //     char my_char;
    //     if (irq_flag == BUTTON_2){
    //         my_char = 'b';
    //     }else if (irq_flag == BUTTON_3){
    //         my_char = 'c';
    //     }else if (irq_flag == BUTTON_4){
    //         my_char = 'd';
    //     }else {
    //         my_char = 'x';
    //     }
    //     // print_char(my_char);
    // }
    
    enable_interrupts();
}

// #include "lib/strings.c"
// int main(){
//     reset_lcd();
//     print_string("HI");
//     lcd_wait();
// }

// char irq(){
    
//     lcd_wait();
//     print_string("bop");

//     // char value = '!';
//     // PORTB[0] = value;
//     // PORTA[0] = RS;
//     // PORTA[0] = RS|E;
//     // PORTA[0] = RS;
//     // DDRB[0] = 0;-
//     // char busy = 1;
//     // while(busy){
//     //     PORTA[0] = RW;
//     //     PORTA[0] = RW|E;
//     //     busy = PORTB[0] & 0b10000000;
//     // }
//     // PORTA[0] = RW;
//     // DDRB[0] = 0b11111111;
    
    
//     // print_char('!');
//     // PORTB[0] = 'x';
//     // PORTA[0] = RS;
//     // PORTA[0] = RS|E;
//     // PORTA[0] = RS;
//     // print_char('x');
// }