LedControl lc=LedControl(12,11,10, 5);
byte number[]={
    0b01000000,
    0b01001000,
    0b01000100,
    0b01001100,
    0b01000010,
    0b01001010,
    0b01000110,
    0b01001110
  };

void Display(int * pointer){

  
  int a=0;
  int numm[]={0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
  
  for (int i=0; i<13; i++){
    if (pointer[i]>0 && pointer[i]<64) {
      numm[i]=pointer[i];
    }
  }



  lc.setRow(0, 0, number[numm[0]/8]);
  lc.setRow(0, 1, number[numm[0]%8]);
  lc.setRow(0, 3, number[numm[1]/8]);
  lc.setRow(0, 4, number[numm[1]%8]);
  lc.setRow(0, 6, number[numm[2]/8]);
  lc.setRow(0, 7, number[numm[2]%8]);
  
  lc.setRow(1, 1, number[numm[3]/8]);
  lc.setRow(1, 2, number[numm[3]%8]);
  lc.setRow(1, 4, number[numm[4]/8]);
  lc.setRow(1, 5, number[numm[4]%8]);
  lc.setRow(1, 7, number[numm[5]/8]);

  lc.setRow(2, 0, number[numm[5]%8]);
  lc.setRow(2, 2, number[numm[6]/8]);
  lc.setRow(2, 3, number[numm[6]%8]);
  lc.setRow(2, 5, number[numm[7]/8]);
  lc.setRow(2, 6, number[numm[7]%8]);

  lc.setRow(4, 1, number[numm[11]/8]);
  lc.setRow(4, 2, number[numm[11]%8]);
  lc.setRow(4, 4, number[numm[12]/8]);
  lc.setRow(4, 5, number[numm[12]%8]);
  
  lc.setRow(3, 0, number[numm[8]/8]);
  lc.setRow(3, 1, number[numm[8]%8]);
  lc.setRow(3, 3, number[numm[9]/8]);
  lc.setRow(3, 4, number[numm[9]%8]);
  lc.setRow(3, 6, number[numm[10]/8]);
  lc.setRow(3, 7, number[numm[10]%8]);

  
}
