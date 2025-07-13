struct A {
    char b;
    char c;
};



struct A get_struct(){
    struct A inner_a;
    inner_a.b = 9;
    inner_a.c = 4;
    return inner_a;
}

char main(){

    struct A some_struct = get_struct();
    return some_struct.b - some_struct.c;

}

char irq(){
    
}
