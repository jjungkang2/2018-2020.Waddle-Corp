#include "Braille.h"

Word w_;
unsigned char update[16];

void Init(){
    for (int i=0; i<26; i++){
      Serial.write(allup[i]);
    }
    for (int i=0; i<26; i++){
      Serial.write(alldw[i]);
    }

    Serial.println("Initialized");
}


void setup()
{
  Serial.begin(115200);
  Serial.println("Hello");

  Init();
  w_.Init();
}

void Update(unsigned char *update){

  w_.Update(update);

  for (int i=0; i<26; i++){
    Serial.write(w_.dot[i]);
  }
  delay(1000);
}

void loop() 
{
  for(int i=0; i < 26; i++){
    Serial.write(allup[i]);
  }
  delay(1000);

  Update(update);
  
  for(int i=0; i < 26; i++){
    Serial.write(alldw[i]);
  }
  delay(1000);
}
