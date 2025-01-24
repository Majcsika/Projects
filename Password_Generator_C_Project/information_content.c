#include "information_content.h"
#include <ctype.h>
#include <math.h>
#include <string.h>


double information_content_of_password(char *password) {
    int alphabet_size = 0;
    double result = 0;
    int _lower = 0;
    int _upper = 0;
    int _digit = 0;
    int _symbol = 0;
    //Have counters for each LUDS group, and increment when an element of that group is present.
    for (int i = 0; password[i] != '\0'; ++i) {
        if (islower(password[i])) {
            ++_lower;
        }
        else if (isupper(password[i])) {
            ++_upper;
        }
        else if (isdigit(password[i])) {
            ++_digit;
        }
        else {
            ++_symbol;
        }
    }
    //Using if's below so that it will check each LUDS group
    if (_lower > 0) {
        alphabet_size = alphabet_size + 26;
    }
    if (_upper > 0) {
        alphabet_size = alphabet_size + 26;
    }
    if (_digit > 0) {
        alphabet_size = alphabet_size + 10;
    }
    if (_symbol > 0) {
        alphabet_size = alphabet_size + 32;
    }

    return result = (strlen(password) * log2((double)alphabet_size));
}
