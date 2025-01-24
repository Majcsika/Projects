#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "alphabet.h"
#include "information_content.h"
#include "pw_generator.h"

int main(int argc, char **argv) {
    // Seed the gen_password function
    srand(time(NULL));

    //Process command line
    if (argc < 3) {
        printf("Usage: %s length quantity [-luds] [alphabet]\n", argv[0]);
        return 1;//Indicates a failure, that's non-zero
    }
    //Read length and quantity
    long length = strtol(argv[1], NULL, 10);//strtol(str, endptr, base)
    long quantity = strtol(argv[2], NULL, 10);

    //Calculate alphabet
    bool alphabet_flags[128];
    memset(alphabet_flags, false, 128 * sizeof(bool));
    //Set all values to false
    if (argc == 3) {
        char arg[] = "-luds";
        process_luds(arg, alphabet_flags);
    }
    else {
        for (int i = 3; i < argc; ++i) {
            if (argv[i][0] == '-') {
                process_luds(argv[i], alphabet_flags);
            }
            else {
                process_alphabet(argv[i], alphabet_flags);
            }
        }
    }
    //Convert alphabet_flags to a string
    char alphabet[128];
    convert_flags(alphabet_flags, alphabet);
    printf("Using alphabet: %s\n", alphabet);

    //Generate passwords
    for (int i = 0; i < quantity; ++i) {
        printf("\nPassword %d:\n", i + 1);
        char password[100];
        gen_password(alphabet, length, password);
        printf("Password: %s\n", password);

        double ic = information_content_of_password(password);
        printf("Information content: %.2lf bits\n", ic);
    }
    return 0;
}

