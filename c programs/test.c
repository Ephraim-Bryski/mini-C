#include "lib/strings.c"
#include "lib/lcd.c"


char* IFR = (char*) 0x600D;
char* IER = (char*) 0x600E;

char BUTTON_1 = 0b10000001;
char BUTTON_2 = 0b10000010;
char BUTTON_3 = 0b10010000;
char BUTTON_4 = 0b10001000;

char main(){

    initialize_lcd();
    
}


char TEST_WIRE = 0b00010000;

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

char block_interrupts(){
    IER[0] = 0b00011011;
    // TODO not sure why this is needed
    // otherwise nothing prints after exiting interrupt
    // lcd_wait();
}
char enable_interrupts(){
    IER[0] = 0b10011011;
}


char count = 'a';

char irq(){
    // block_interrupts();
    char irq_flag = IFR[0];
    // char 
    
    if (irq_flag == BUTTON_1){
        print_char(count);
        count = 'a';
    }else if (irq_flag == BUTTON_4){
        count += 1;
    }
    

    // while(1){}

    // enable_interrupts();
    // // block_interrupts();    
    
    // if (irq_flag == BUTTON_1){
    //     print_char(count);
    //     count = 'a';
    // }else{
    //     // lcd_wait();
    //     count += 1;
    // }
    // print_char('d');
    
    // block_interrupts();
    // if (PORTA[0] & TEST_WIRE){
    //     print_char('Y');
    // }else{
    //     print_char('N');
    // }
    // enable_interrupts();
}