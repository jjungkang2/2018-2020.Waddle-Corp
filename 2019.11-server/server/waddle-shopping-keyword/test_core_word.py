from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import NavigableString
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from multiprocessing import Pool
import json
from konlpy.tag import Twitter
from collections import Counter

def check_what_is_this(A):
    if '0'<=A<='9' or A is '.':
        return 'number'
    elif '가'<=A<='힣':
        return 'korean'
    elif 'A'<=A<='Z' or 'a'<=A<='z':
        return 'korean'
    return 'else'

def erasing_unit(temp1):
    remove_list=[]

    for idx in range(len(temp1)):
        if check_what_is_this(temp1[idx]) is 'number':
            remove_list.append(idx)
            unit=""
            is_unit1=True
            is_unit2=False

            while 1:
                idx+=1
                if idx>=len(temp1):
                    if is_unit1 is True:
                        del remove_list[-1]
                    elif is_unit2 is True:
                        remove_list.append(idx)
                    break

                if is_unit1 is False and is_unit2 is False and check_what_is_this(temp1[idx]) is 'number':
                    remove_list.append(idx)
                    is_unit1 = True
                elif is_unit1 is False and is_unit2 is True and check_what_is_this(temp1[idx]) is 'number':
                    del remove_list[-1]
                    is_unit2 = False
                    unit=""
                elif is_unit1 is False and is_unit2 is True and check_what_is_this(temp1[idx]) is 'korean':
                    unit = unit+temp1[idx]
                elif is_unit1 is False and is_unit2 is True and check_what_is_this(temp1[idx]) is 'else':
                    remove_list.append(idx)
                    is_unit2 = False
                    unit=""
                elif is_unit1 is True and is_unit2 is False and check_what_is_this(temp1[idx]) is 'korean':
                    is_unit1 = False
                    is_unit2 = True
                    unit = unit+temp1[idx]
                elif is_unit1 is True and is_unit2 is False and check_what_is_this(temp1[idx]) is 'else':
                    del remove_list[-1]
                    is_unit1 = False
                    unit=""
                
            break;

    while(len(remove_list)):
        idx1 = remove_list[-2]
        idx2 = remove_list[-1]
        
        temp1 = temp1[0:idx1] + temp1[idx2+1:len(temp1)]

        del remove_list[-1]
        del remove_list[-1]

    return temp1
        


def product_crawl(line):

    
    line = line[0:-1] #'\n' out
    print(line)
    temp = line+', '
    initial_link = "https://www.coupang.com/np/search?component=&q="+line+"&channel=user"

    print('start!')

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    # options.add_argument('--headless')

    driver = webdriver.Chrome("./chromedriver", options=options)
    driver.get(initial_link)

    print('web_opened')
    # WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")

    #wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#breadcrumb > li:nth-child(2) > a')))

    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')


    products_list=[]
    products_seperate_list=[]
    products_final_list=[]
    # options_remove_list=["쿠팡서비스", "카테고리", "상품 상태", "별점", "가격"]
    unit_list=[]
    name_count=[]
    option_list=[]
    option_list.append("단일 색상")
    option_list.append("혼합 색상")
    option_list.append("블랙")
    option_list.append("네이비")
    option_list.append("그레이")
    option_list.append("실버")
    option_list.append("레드")
    option_list.append("오렌지")
    option_list.append("옐로우")
    option_list.append("그린")
    option_list.append("블루")
    option_list.append("바이올렛")
    option_list.append("보라")
    option_list.append("핑크")
    option_list.append("화이트")
    option_list.append("브라운")
    option_list.append("골드")
    option_list.append("베이지")
    option_list.append("투명")
    

    print()
    print("processing..")
    print()

    #getting brand name
    if len(soup.select("div#searchBrandFilter")) is 0:
        temp = temp+'error\n'
        txt_File.write(temp)
        driver.close()
        return
    
    for body in soup.select("div#searchBrandFilter")[0].select("ul")[0].select("li"):
        option_list.append(body.select("label")[0].text)

    for product in range(len(soup.select("li.search-product"))):
        if product>30:
            break
        product = soup.select("li.search-product")[product]
        name = product.select("div.name")[0].text
        name = erasing_unit(name)

        products_list.append(name)

    for name in products_list:
        name = name.replace(",", "")
        name = name.replace("-", "")
        name = name.replace("[", "")
        name = name.replace("]", "")
        name = name.replace("&", "")    
        name = name.replace(" + ", " ")
        name = name.replace(" x ", " ")
        name = name.split(" ")
        name = list(filter(None, name))
        products_seperate_list.append(name)

    for product in products_seperate_list:
        for option in option_list:
            if option in product:
                product.remove(option)
        products_final_list.append(product)

    word_name = []
    word_count = []

    for name in products_final_list:
        for word in name:
            if word in word_name:
                idx = word_name.index(word)
                word_count[idx] = word_count[idx]+1
            else:
                word_name.append(word)
                word_count.append(1)

    idx1=-1
    idx2=-1
    idx3=-1
    max1=0
    max2=0
    max3=0

    for idx in range(len(word_count)):
        if word_count[idx]>max1:
            idx3 = idx2
            idx2 = idx1
            idx1 = idx
            max3 = max2
            max2 = max1
            max1 = word_count[idx]
        elif word_count[idx]>max2:
            idx3 = idx2        
            idx2 = idx
            max3 = max2
            max2 = word_count[idx]
        elif word_count[idx]>max3:
            idx3 = idx
            max3 = word_count[idx]

    print(f"First word {word_name[idx1]} is called {max1} times")
    print(f"Second word {word_name[idx2]} is called {max2} times")
    print(f"Third word {word_name[idx3]} is called {max3} times")

    temp = temp+word_name[idx1]+', '+str(max1)+', '+word_name[idx2]+', '+str(max2)+', '+word_name[idx3]+', '+str(max3)+'\n'
    txt_File.write(temp)

    driver.close()


# get hash list from txt file
txt_file = open('test.txt', 'r', encoding='utf-8')
txt_File = open('test_result.txt', 'a', encoding='utf-8')

for line in txt_file.readlines():
    product_crawl(line)

# if __name__=='__main__':
#     pool = Pool(processes=5)
#     pool.map(product_crawl, txt_file.readlines())