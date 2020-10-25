#ifndef WORDTOBRAILLE_H
#define WORDTOBRAILLE_H

#include "BinaryConvert.h"
#include <stdlib.h>

class Braille;

class Word{
public:
	Word();
	void Init(char *in_word);
	Braille WordToBraille();
	int WordLen();
	char get(int index);
	void FreeWord();
  int binlen;
private:
	char *word;
	int wordlen;
};

#endif
