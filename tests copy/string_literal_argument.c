



char* change_string(char* a, int idx){
    a[idx] = 'o';
    return a;
}


char main(){
    // passing string literals is a bit tricky cause pushing the chars can mess up the parameter stack
    // for now im resolving it by creating a dummy variable first
    char* new_string = change_string("hullx",3);

    return new_string[3];

}
