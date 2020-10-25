from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup, SoupStrainer
from bs4 import NavigableString
import requests
import time
import json
import pymysql
import threading
import datetime
import boto3

### execute SQL Query
def execute(sql, flag=False):
    with db.cursor() as cursor:
        cursor.execute(sql)
        if flag:
            result = cursor.fetchall()
            db.commit()
            return result
        db.commit()
        return None

def product_crawl(email, orderId):

    while True :
        print(orderId)
        print('start '+str(datetime.datetime.now(datetime.timezone.utc)))

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        # driver = webdriver.Chrome("./chromedriver.exe", options=options)
        driver = webdriver.Chrome(options=options)

        try:
            initial_link = "https://my.coupang.com/purchase/detail/"+orderId
            driver.get('about:blank')
            driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
            driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
            driver.execute_script("const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")
            driver.get(initial_link)
            driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
            driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
            driver.execute_script("const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")
            driver.implicitly_wait(3)

            driver.find_element_by_id('login-email-input').send_keys(email)
            driver.find_element_by_id('login-password-input').send_keys('wdwd0417!')
            driver.find_element_by_xpath('/html/body/div[1]/div/div/form/div[5]/button').click()
            driver.implicitly_wait(3)
            driver.get(initial_link)
            driver.implicitly_wait(3)

            # element = WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, '#my__container > div.my-purchase-view > div.my-purchase-view__unit-group > table:nth-child(2) > tbody > tr:nth-child(3) > td.my-order-unit__area-item-group > div:nth-child(4) > div > div.my-order-unit__item-info > a'))
            # )

            soup = BeautifulSoup(driver.page_source, 'lxml')

            check_error = soup.select('#contents > h3')
            if len(check_error) != 0:
                driver.close()
                driver.quit()
                product_crawl('waddle@waddlelab.com', orderId)
                return

            meta = soup.select('table.my-order-unit')
            if len(meta) != 0:
                break
            else:
                driver.close()
                driver.quit()

        except Exception as e:
            print("error from product_crowl")
            print(e)
            driver.close()
            driver.quit()

    Status_dict = {'결제완료':'ordered', '상품준비중':'deliver request', '배송 준비중': 'deliver request', '배송시작':'delivering', '배송중': 'delivering', '배송완료': 'delivered', '반품접수': 'refund requesting'}

    for product in meta:
        status_meta = product.select('tbody > tr:nth-child(1) > td > meta')[0]
        product_meta = product.select('tbody > tr:nth-child(3) > td > meta')

        print(status_meta)
        json_meta = json.loads(status_meta['data-log-payload'])
        P_STATUS = Status_dict[json_meta['deliveryStatus']]
        P_DELIVERYDATE = json_meta['pddMessage']

        for item_meta in product_meta:
            json_meta = json.loads(item_meta['data-log-payload'])
            P_ORDERID = json_meta['orderId']
            P_OPTIONID = json_meta['vendorItemId']
            execute(f"""UPDATE Ordered SET Status='{P_STATUS}', DeliveryDate='{P_DELIVERYDATE}' WHERE OrderID='{P_ORDERID}' AND ProductOptionID='{P_OPTIONID}';""")

    update_list = execute(f"""SELECT Status FROM Ordered WHERE OrderID='{P_ORDERID}';""", True)
    update_list = list(set([x[0] for x in update_list]))
    if 'ordered' in update_list:
        execute(f"""UPDATE Purchase SET Status='ordered' WHERE OrderID='{P_ORDERID}';""")
    elif 'deliver request' in update_list:
        execute(f"""UPDATE Purchase SET Status='deliver request' WHERE OrderID='{P_ORDERID}';""")
    elif 'delivering' in update_list:
        execute(f"""UPDATE Purchase SET Status='delivering' WHERE OrderID='{P_ORDERID}';""")
    elif 'delivered' in update_list:
        execute(f"""UPDATE Purchase SET Status='delivered' WHERE OrderID='{P_ORDERID}';""")

    driver.close()
    driver.quit()

def send_push(message, token):
    print('send_push')
    try:
        
        arn = 'arn:aws:sns:ap-northeast-2:115937545464:endpoint/APNS_SANDBOX/Waddleshopping/15ca02ed-f092-34e7-a968-51194f9d086c'
        sns = boto3.client('sns', region_name='ap-northeast-2', aws_access_key_id='AKIARV7TKRT4GOQN7KZ4', aws_secret_access_key='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')
        endpoint = execute(f"""SELECT EndPoint FROM User WHERE Token='{token}';""", True)[0][0]

        apns_dict = {'aps':{'alert':'inner message','sound':'mySound.caf'}}
        apns_dict['aps']['alert'] = message
        apns_string = json.dumps(apns_dict,ensure_ascii=False)
        message = {'default':'default message','APNS':apns_string}
        messageJSON = json.dumps(message,ensure_ascii=False)
        # sns.publish(Message=messageJSON, TargetArn=endpoint, MessageStructure='json')

    except Exception as e:
        print(e)
        print('error from send_push')

def watch():
    while True:
        today = datetime.datetime.now(datetime.timezone.utc)
        time_now = int(today.strftime("%H"))
        confirmed_date = today.date() - datetime.timedelta(30)
        confirmed_date = confirmed_date.strftime("%m/%d")
        confirm_date = today.date() - datetime.timedelta(10)
        confirm_date = confirm_date.strftime("%m/%d")
        review_date = today.date() - datetime.timedelta(3)
        review_date = review_date.strftime("%m/%d")

        if time_now>=1 and time_now<=13:
            db = pymysql.connect(host='waddle-shopping-db.cn3btnlhdzhq.ap-northeast-2.rds.amazonaws.com',
                port=3306,
                user='admin',
                passwd='Waddlecorp#',
                db='User2',
                charset='utf8') 
                 
            if time_now == 5: #3시
                update_list = execute(f"""SELECT Token, ProductID, ProductName, ProductOptionID, OrderID, DeliveryDate FROM Ordered WHERE Status='delivered';""", True)
                for date in update_list:
                    print(date)
                    if "오늘" in date[5]:
                        new_date = date[5].replace("오늘(", "")
                        new_date = new_date.replace(")", "요일")
                        execute(f"""UPDATE Ordered SET DeliveryDate='{new_date}' WHERE ProductID={date[1]} AND ProductOptionID='{date[3]}' AND OrderID='{date[4]}';""")
                    if date[5].split()[1] == review_date:
                        send_push(date[2]+"의 리뷰를 남겨주세요!", date[0])
                    elif date[5].split()[1] == confirm_date:
                        send_push(date[2]+"이 마음에 드셨나요?\n 마음에 드셨다면 구매 확정을 해주세요!", date[0])
                    elif date[5].split()[1] == confirmed_date:
                        execute(f"""UPDATE Ordered SET Status='confirmed' WHERE ProductID={date[1]} AND ProductOptionID='{date[3]}' AND OrderID='{date[4]}';""")
                    
            
            update_list = execute(f"""SELECT OrderID FROM Ordered WHERE (Status='ordered' or Status='deliver request' or Status='delivering');""", True)
            # update_list = execute(f"""SELECT OrderID FROM Ordered WHERE Status='delivering' AND DeliveryDate='';""", True)
            update_list = list(set([x[0] for x in update_list]))

            for orderId in update_list:
                if orderId.isdigit():
                    print(orderId+', '+str(update_list.index(orderId))+'/'+str(len(update_list)))
                    product_crawl('jihyuk0525@naver.com', orderId)
                    
            db.close()

            print("finish!")

        time.sleep(3600)


if __name__ == '__main__':

    db = pymysql.connect(host='waddle-shopping-db.cn3btnlhdzhq.ap-northeast-2.rds.amazonaws.com',
                    port=3306,
                    user='admin',
                    passwd='Waddlecorp#',
                    db='User2',
                    charset='utf8')       

    t = threading.Thread(target=watch)
    t.start()