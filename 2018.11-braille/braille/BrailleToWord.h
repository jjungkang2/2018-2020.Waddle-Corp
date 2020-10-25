#ifndef BRAILLETOWORD_H
#define BRAILLETOWORD_H

#include "BinaryConvert.h"
#include <stdlib.h>

class Word;

class Braille {
public:
	Braille();
	void Init(int *in_bin, int in_binlen);
	Word BrailleToWord();
	int BrailleLen();
	int get(int index);
	void FreeBraille();
private:
	int *bin, binlen, wordlen;
};

#endif
