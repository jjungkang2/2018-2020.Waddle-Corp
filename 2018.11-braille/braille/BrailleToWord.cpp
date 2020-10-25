#include "BrailleToWord.h"
#include "WordToBraille.h"

Braille::Braille(){}

void Braille::Init(int *in_bin, int in_binlen){
	bin = in_bin;
	binlen = in_binlen;
}

Word Braille::BrailleToWord(){
	char prevchar, *word = (char*)malloc(sizeof(char) * 500);
	int langmode = 0;

	wordlen = 0;
	
	for(int i = 0; i < binlen; i++){
		prevchar = BinToAscii(bin[i]);

		if(langmode == 0){
			if(prevchar == '#'){
				langmode = 1;
			}
		}
		else{
			if(prevchar == ';'){
				langmode = 0;
			}
			else if(prevchar >= 'k' && prevchar <= 'z'){
				langmode = 0;
			}
			else if(prevchar == ' '){
				langmode = 0;
			}
			else if(prevchar == '6' || prevchar == '8'){
				langmode = 0;
			}
		}

		if(langmode == 0){
			if(prevchar >= 'a' && prevchar <= 'z'){
				word[wordlen++] = prevchar;
			}
			else if(prevchar == '4'){
				word[wordlen++] = prevchar;
			}
			else if(prevchar == '6'){
				word[wordlen++] = '!';
			}
			else if(prevchar == '8'){
				word[wordlen++] = '?';
			}
			else if(prevchar == ' '){
				word[wordlen++] = ' ';
			}
		}
		else{
			if(prevchar >= 'a' && prevchar <= 'i'){
				word[wordlen++] = prevchar - 'a' + '1';
			}
			else if(prevchar == 'j'){
				word[wordlen++] = '0';
			}
			else if(prevchar == '4'){
				word[wordlen++] = '.';
			}
		}
	}
	
	word[wordlen] = '\0';

	Word return_word;
  return_word.Init(word);

	return return_word;
}

int Braille::BrailleLen(){
	return binlen;
}

int Braille::get(int index){
	return bin[index];
}

void Braille::FreeBraille(){
	free(bin);
	return;
}
