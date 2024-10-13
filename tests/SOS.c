struct A {
    char b;
    char c;
};

struct AA {
    char d;
    struct A inside;
    char e;
};


char main(){
    struct A my_a;
    my_a.b = 4;
    my_a.c = 9;

    struct AA my_aa;
    my_aa.inside = my_a;
    my_aa.d = 20;
    my_aa.e = 30;
    return my_aa.inside.b;
}