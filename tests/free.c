
#include "lib/allocator.c"
#include "lib/arrays.c"

char main(){

    
    struct Array a = create_array(5);

    int base_address = (int) a.items;

    struct Array b = create_array(5);

    delete_array(a);

    struct Array a_same_size = create_array(5);

    if ((int) a_same_size.items != base_address){
        return 1;
    }

    struct Array a_bigger = create_array(6);

    if ((int) a_bigger.items == base_address){
        return 1;
    }

    return 0;

    
}

char irq(){
    
}
