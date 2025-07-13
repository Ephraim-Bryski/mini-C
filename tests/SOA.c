struct A {
    char* an_array;
    char an_char;
};

char main(){
    char some_array[] = {3,4,5};
    struct A a;
    a.an_array = some_array;
    return a.an_array[1] + a.an_array[2];
}

char irq(){
    
}
