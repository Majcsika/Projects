#ifndef ALPHABET_H
#define ALPHABET_H
#include <stdbool.h>

void process_alphabet(char *arg, bool *alphabet_flags);
void process_luds(char *arg, bool *alphabet_flags);
void convert_flags(bool *alphabet_flags, char *output);

#endif