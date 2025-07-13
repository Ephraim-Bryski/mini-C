struct A {
    char b;
    char c;
};



struct A get_struct(){
    struct A inner_a;
    inner_a.c = 4;
    inner_a.b = 9;
    return inner_a;
}

char main(){

    char c_val = get_struct().c;
    char b_val = get_struct().b;
    return b_val + c_val;
}

char irq(){
    
}
