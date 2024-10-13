
#include "lib/allocator.c"
#include "lib/arrays.c"

char main(){

    
    struct Array a = create_array(2);

    struct Array b = create_array(5);

    b.items[1] = 100;

    a.items[1] = 2000;

    struct Array combined = concatenate(a, b);

    
    return (char) index(combined, 3);
    

}