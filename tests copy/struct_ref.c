struct A {
    char a;
    char b;
};

char change_struct(struct A* my_struct){
    my_struct -> a = 30; 
    my_struct -> b = 24;
}

char main(){

    struct A my_struct;
    
    struct A* struct_ref = &my_struct;

    change_struct(struct_ref);
    
    return struct_ref -> a - struct_ref -> b;
}