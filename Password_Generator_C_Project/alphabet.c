#include "alphabet.h"
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

void process_alphabet(char *arg, bool *alphabet_flags){
    for (int i = 0; arg[i] != '\0'; ++i) {
        if (isgraph(arg[i])) {
            alphabet_flags[(int)arg[i]] = true;
        }
    }
}

void process_luds(char *arg, bool *alphabet_flags){
    for (int i = 1; arg[i] != '\0'; ++i) {
        if (arg[i] == 'l') {
            for (int j = 97; j < 123; ++j) {
                alphabet_flags[j] = true;
            }
        }
        else if (arg[i] == 'u') {
            for (int j = 65; j < 91; ++j) {
                alphabet_flags[j] = true;
            }
        }
        else if (arg[i] == 'd') {
            for (int j = 48; j < 58; ++j) {
                alphabet_flags[j] = true;
            }
        }
        else if (arg[i] == 's') {
            for (int j = 33; j < 48; ++j) {
                alphabet_flags[j] = true;
            }
            for (int j = 58; j < 65; ++j) {
                alphabet_flags[j] = true;
            } 
            for (int j = 91; j < 97; ++j) {
                alphabet_flags[j] = true;
            }   
            for (int j = 123; j < 127; ++j) {
                alphabet_flags[j] = true;
            }   
        }          
    }
}

void convert_flags(bool *alphabet_flags, char *output){
    int j = 0;
    for (int i = 0; i < 128; ++i) {
        if (alphabet_flags[i] == 1) {
            output[j] = i;
            ++j;
        }
    }
    output[j] = '\0';
}
