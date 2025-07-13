struct A {
    int b;
    char c;
};

char main (){
    struct A A1;
    struct A A2;

    A1.b = 5;
    A1.c = 9;
    A2.b = A1.c-A1.b;
    A2.c = A2.b*3;
    return A2.c;
}