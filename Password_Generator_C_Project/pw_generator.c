#include "pw_generator.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void gen_password(char *alphabet, long length, char *password) {
    int a = strlen(alphabet);
    for (int i = 0; i < length; ++i) {
        int x = rand_int(0, a - 1);
        password[i] = alphabet[x];
    }
    password[length] = '\0';
}

int rand_int(int a, int b) {
    //Use sample rejection
    int range = b - a + 1;
    int discarding_limit = RAND_MAX - (RAND_MAX % range);

    for (;;) {
        // Generates in [0, RAND_MAX]
        int initial = rand();
        if (initial > discarding_limit) {
            //Try again
            continue;
        }
    
        //Scale to a [0, b - a + 1]
        int scaled = initial % range;
        //Shift to [a, b]
        int shift = scaled + a;
        return shift;
    }
}
