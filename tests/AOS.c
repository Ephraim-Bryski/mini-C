
struct A {
    int b;
    char inbetween;
    int c;
};



char main(){
    struct A a1;
    struct A a2;


    a1.b = 10;
    a1.c = 20;
    a2.b = 30;
    a2.c = 40;

    struct A AOS[] = {a1, a2};
     
    return AOS[1].b + AOS[1].c;
    

}