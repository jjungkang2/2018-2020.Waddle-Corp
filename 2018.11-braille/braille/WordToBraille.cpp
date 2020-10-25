#include "BrailleToWord.h"
#include "WordToBraille.h"

Word::Word(){}

void Word::Init(char *in_word){
  word = in_word, wordlen = 0;

  while(word[wordlen] != '\0'){
    wordlen++;
  }
}

Braille Word::WordToBraille(){
	int *bin = (int*)malloc(sizeof(int) * 500), langmode = 0;

	binlen = 0;

	for(int i = 0; i < wordlen; i++){
		if(word[i] >= 'a' && word[i] <= 'z'){
			if(langmode == 1){
				bin[binlen++] = AsciiToBin(';');
				langmode = 0;
			}
			bin[binlen++] = AsciiToBin(word[i]);
		}
		else if(word[i] >= '0' && word[i] <= '9'){
			if(langmode == 0){
				bin[binlen++] = AsciiToBin('#');
				langmode = 1;
			}
			if(word[i] == '0'){
				bin[binlen++] = AsciiToBin('j');
			}
			else{
				bin[binlen++] = AsciiToBin(word[i] - '1' + 'a');
			}
		}
		else if(word[i] == '.'){
			bin[binlen++] = AsciiToBin('4');
		}
		else if(word[i] == '!'){
			langmode = 0;
			bin[binlen++] = AsciiToBin('6');
		}
		else if(word[i] == '?'){
			langmode = 0;
			bin[binlen++] = AsciiToBin('8');
		}
		else if(word[i] == ' '){
			langmode = 0;
			bin[binlen++] = AsciiToBin(' ');
		}
	}

  Braille return_bin;
  return_bin.Init(bin, binlen);

	return return_bin;
}

int Word::WordLen(){
	return wordlen;
}

char Word::get(int index){
	return word[index];
}

void Word::FreeWord(){
	free(word);
	return;
}
