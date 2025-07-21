#include "strings.c"



// apparently allocators typically use linked lists, with each element having info on its size, and pointing to the next

// here i instead have all of the information on location separate from the data

// also, it's all done inside a single malloc (no OS requests or anything fancy)





struct bk_block {
    int* start;
    int* end;
};



// size: n_elemnts_limit*sizeof(int)                                   
// <------------------------------- DATA ----------------------------->

// size: n_allocate_limit*sizeof(bk_block)
// <-- BOOKKEEPING -->

// size: sizeof(int)
// <-NUM OF ALLOCATIONS->



int* HEAP_BASE = (int*) 10;
int N_ELEMENTS_LIMIT = 20;
int N_ALLOCATE_LIMIT = 4; 

char COUNT_INITIALIZED = 0;

int int_size = 2;

struct bk_block* BK_LOCATION(){
    return (struct bk_block*) ((int) HEAP_BASE + N_ELEMENTS_LIMIT * int_size);
}

int* COUNT_LOCATION(){
    struct bk_block sample_block_for_size;  // caue i dont support sizeof(type)
    int bk_block_size = sizeof(sample_block_for_size);
    return (int*) ((int) BK_LOCATION() + N_ALLOCATE_LIMIT*bk_block_size);
}



int* my_malloc(int n_items){

    if (!COUNT_INITIALIZED){
        COUNT_LOCATION()[0] = 0;
        COUNT_INITIALIZED = 1;
    }

    int n_allocations = COUNT_LOCATION()[0];

    if (n_allocations == N_ALLOCATE_LIMIT){
        error("cant make any more allocations :(");
    }

    // search for a space:

    int* selected_location = (int*) 0;
    int selected_bk_idx;
    int size_items = n_items * int_size;

    int i;
    for (i=0;i<=n_allocations;i+=1){
        int* space_start;
        if (i == 0){
            space_start = HEAP_BASE;
        }else{
            space_start = BK_LOCATION()[i-1].end;
        }
        int* space_end;
        if (i == n_allocations){
            space_end = (int*) BK_LOCATION();
        }else{
            space_end = BK_LOCATION()[i].start;
        }
        int size_difference = (int) space_end - (int) space_start;
        if (size_difference >= size_items){
                    
            selected_location = space_start;
            selected_bk_idx = i;
            break;
        }
    }

    if(!selected_location){
        error("no space :O");
    }

    // like c's malloc, i won't write data, i'll just allocate memory
    // // write the data:
    // for (i=0;i<n_items;i+=1){
    //     selected_location[i] = data[i];
    // }

    // insert the bookkeeping block, shifting the blocks after it one to the right:
    struct bk_block new_block;
    new_block.start = selected_location;
    new_block.end = (int*) ((int) selected_location + size_items);

    for (i=n_allocations; i>selected_bk_idx; i-=1){

        BK_LOCATION()[i] = BK_LOCATION()[i-1];
    }
    
    BK_LOCATION()[selected_bk_idx] = new_block;

    // increment the number of allocations

    COUNT_LOCATION()[0] +=1;


    return selected_location;




}


int my_free(int* ptr_to_free){

    int found_ptr = 0;

    // allocate had to search and shift as two loops since it would overwrite if shifting left to right
    // but free doesnt have this issue so i can do it one run :)

    int i;
    for (i=0;i<COUNT_LOCATION()[0];i+=1){
    

        struct bk_block block = BK_LOCATION()[i];

        if (found_ptr){
            BK_LOCATION()[i-1] = block;
        }

        if (block.start == ptr_to_free){
            found_ptr = 1;
        }
    }

    if (!found_ptr){
        error("doesnt point to any data ):<");
    }

    COUNT_LOCATION()[0] -= 1;
    


}



// int print_allocations(){

//     print_newline();
//     print_string("number of allocations: ");
//     _print_int(COUNT_LOCATION()[0]);
//     print_newline();
    
//     int i;
//     for (i=0;i<COUNT_LOCATION()[0];i+=1){

//         struct bk_block block = BK_LOCATION()[i];
//         int relative_start = (int)block.start-(int)HEAP_BASE;
//         int relative_end = (int)block.end-(int)HEAP_BASE;
//         _print_int(relative_start);
//         print_string(" to ");
//         _print_int(relative_end);
//         print_string(" [");
        

//         int location;

//         for (location = (int) block.start; location< (int) block.end; location+=int_size){
//             int* location_address = (int*) location;
//             _print_int(location_address[0]);
//             print_char(',');
//         }
        
        
//         print_string("]");
//         print_newline();
//     }

//     print_newline();

// }


