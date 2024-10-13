char main(){
    char a = 1;
    char b = 1;
    char c;
    char i;
    for (i=0;i<5;i+=1){
        c = a + b;
        a = b;
        b = c;
    }
    return c;
}