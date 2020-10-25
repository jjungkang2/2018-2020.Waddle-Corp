import csv

MAX = 100

CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
JONGSUNG_LIST = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

def hash_key(A):
    temp1 = ord(A[0])%MAX if len(A)>0 else MAX-1
    temp2 = ord(A[1])%MAX if len(A)>1 else MAX-1
    return temp1*temp2

#JAUM 12593~12622
#MOUM 12623~12643
def seperate_korean(word_list):
    r_lst = []
    for w in list(word_list.strip()):
        #if Korean
        if '가'<=w<='힣':
            # 588 = (num of JUNGSUNG) * (num of JONGSUNG)
            # 28 = (num of JUNGSUNG)
            ch1 = (ord(w) - ord('가'))//588
            ch2 = ((ord(w) - ord('가')) - (588*ch1)) // 28
            ch3 = (ord(w) - ord('가')) - (588*ch1) - 28*ch2
            r_lst.append(CHOSUNG_LIST[ch1])
            r_lst.append(JUNGSUNG_LIST[ch2])

            # skip if non JONGSUNG
            if ch3 is not 0: 
                r_lst.append(JONGSUNG_LIST[ch3])
                
        #if English or Number
        else:
            r_lst.append(w)
    return r_lst

def solve():
    hash_list = []

    # initialize hash list
    for i in range(MAX**2):
        hash_list.append([])

    # read CSV File and collect words
    for line in CSV_File:
        if len(line[0]) is not 0:
            txt_file.write(line[0]+'\n')

        if len(line[1]) is not 0:
            temp = line[1]
            temp = temp.split(';')
            for word in temp:
                if len(word) is not 0:
                    txt_file.write(word.strip()+'\n')



CSV_file = open('test.csv', 'r', encoding='utf-8')
CSV_File = csv.reader(CSV_file)
txt_file = open('test.txt', 'w', encoding='utf-8')

solve()

CSV_file.close()
txt_file.close()