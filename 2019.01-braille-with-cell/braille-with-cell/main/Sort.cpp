#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <queue>
using namespace std;

struct Key{
  int press1;
  int press2 = 0;
};

typedef enum Category{
   Drag = 0,
   Number = 1,
   Enter = 10,
   Backspace = 11,
   UpCursor = 20,
   DownCursor = 21,
   LeftCursor = 22,
   RightCursor = 23,
   UpVoiceOver = 30,
   DownVoiceOver = 31,
   LeftVoiceOver = 32,
   RightVoiceOver = 33,
   error = -1
}Category;

Category Sort(struct Key key){ 

	if (key.press2 != 0) return Drag;

	if (0<key.press1 && key.press1<64) return Number;

	switch(key.press1){
		case 0b0000000001000000 : return Enter; break;
		case 0b0000000010000000 : return Backspace; break;
		case 0b0000000100000000 : return UpCursor; break;
		case 0b0000001000000000 : return DownCursor; break;
		case 0b0000010000000000 : return LeftCursor; break;
		case 0b0000100000000000 : return RightCursor; break;
		case 0b0001000000000000 : return UpVoiceOver; break;
		case 0b0010000000000000 : return DownVoiceOver; break;
		case 0b0100000000000000 : return LeftVoiceOver; break;
		case 0b1000000000000000 : return RightVoiceOver; break;
		default : return error; break;
	}
}
