#ifndef BRAILLE_H
#define BRAILLE_H

#include <stdlib.h>
 
class Word{
public:
	Word();
  void Update(unsigned char *);
  void Convert(unsigned char *);
	void Init();
	unsigned char dot[26];
};

extern unsigned char allup[26];
extern unsigned char alldw[26];
                          
#endif
