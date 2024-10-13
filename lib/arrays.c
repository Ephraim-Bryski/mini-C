
#include "strings.c"
#include "allocator.c"

int HEAP_POINTER = 0;



struct Array {
    int length;
    int* items;
};




struct Array create_array(int n_items){
    struct Array array;
    array.length = n_items;
    array.items = my_malloc(n_items);
    return array;
}


struct Array create_array_from_ptr(int* ptr, int n_items){
    // takes the values in an array (presumably on the stack) and copies them to the heap allocation
    struct Array array = create_array(n_items);
    int i;
    for (i=0;i<n_items;i+=1){
        array.items[i] = ptr[i];
    }
    return array;
}




int delete_array(struct Array array){
    my_free(array.items);
}

int index(struct Array array, int index){
    if (index >= array.length){
        error("out of bounds");
    }
    return array.items[index];
}  






int append(struct Array* array, int item){

    int* old_reference = array -> items;

    int new_length = array -> length + 1;


    int* new_reference = my_malloc(new_length);

    // obviously super inefficient
    // only need to copy everything over if the allocation is the exact size of the array
    // ideally my allocator would have a reallocate function that would figure out if copying is required
    int i;
    for (i=0;i<new_length;i+=1){
        new_reference[i] = array->items[i];
    }

    array -> length = new_length;
    array -> items = new_reference;
    array -> items[new_length-1] = item;

    my_free(old_reference);
    
}


int pop(struct Array* array){

    int new_length = array -> length - 1;
    array -> length = new_length;
    int last_item = array -> items[new_length];
    return last_item;
    
}




struct Array concatenate(struct Array arr1, struct Array arr2){

    int* old_reference1 = arr1.items;
    int* old_reference2 = arr2.items;

    int combined_length = arr1.length + arr2.length;

    struct Array combined_arr = create_array(combined_length);

    int i=0;
    for (i=0;i<arr1.length;i+=1){
        combined_arr.items[i] = arr1.items[i];
    }

    for(i=0;i<arr2.length;i+=1){
        int combined_i = arr1.length + i;
        combined_arr.items[combined_i] = arr2.items[i];
    }

    my_free(old_reference1);
    my_free(old_reference2);

    return combined_arr;
}



int print_array(struct Array array){
    
    _print_char('[');
    int idx;
    for (idx=0; idx<array.length; idx+=1){
        _print_int(array.items[idx]);

        if (idx+1 < array.length){
            _print_char(',');
        }
    }
    
    _print_char(']');
    print_newline();
}

int print_array_info(struct Array array, char* name){
    print_string(name);
    print_string(" location: ");
    _print_int(array.items);
    print_newline();

    print_string(name);
    print_string(" size: ");
    _print_int(array.length);
    print_newline();
}

