char fib(char a){
    if (a==0){
        return 1;
    }
    if (a==1){
        return 1;
    }
    return fib(a-1) + fib(a-2);
}


char main(){
    return fib(6);
}