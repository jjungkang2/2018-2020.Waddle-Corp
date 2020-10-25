#include "BinaryConvert.h"

char BinToAscii(int b){
	if(b < 0 || b >= 64) return '\0';
	return bin_to_ascii[b];
}

int AsciiToBin(char c){
	return ascii_to_bin[(int)c];
}