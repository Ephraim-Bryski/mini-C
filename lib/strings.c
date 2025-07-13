#include "lcd.c"

#include <stdio.h>
// these are only called for gcc
// for my compiler these are intrinsics and these definitions are ignored
// also only used for avr
// int _print_int(int value){
//     printf("%d", value);
// }
// int _print_char(char character){
//     printf("%c", character);
// }
int _halt(){
    printf("\n\nExecution would be halted on my compiler.\n\n");
}


int str_length(char* string){
    int idx = 0;
    while(1){
        char string_char = string[idx];
        if (string_char == 0){
            return idx;
        }
        idx += 1;
    }
}


int print_newline(){
    print_char(10);
}

int print_string(char* string){

    int string_length = str_length(string);
    int i = 0;
    for (i=0;i<string_length;i+=1){
        print_char(string[i]);
    }
}

int error(char* message){
    print_string("ERROR: ");
    print_string(message);
    _halt();
}

