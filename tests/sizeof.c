char main(){
    int a[] = {3,4,5,6};


    char sizeof_array = sizeof(a);

    if (sizeof_array != 8){
        return 0;
    }

    int* b = a;

    int sizeof_ptr = sizeof(b);

    if (sizeof_ptr != 2){
        return 0;
    }


    int c = 20;

    if (sizeof(c) != 2){
        return 0;
    }


    return 1;
}

char irq(){
    
}
