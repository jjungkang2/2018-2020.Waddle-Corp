import pymysql
import os
import random

import json
import requests
import base64

import datetime
import secrets


db = None


def base64_encode(str):
    b = str.encode("UTF-8")
    e = base64.b64encode(b)
    r = e.decode("UTF-8")

    return r


def get_token():
    url = 'https://sms.gabia.com/oauth/token'
    payload = 'grant_type=client_credentials'
    api_key = '0d416e574631291a80fe34aa8e2761a6'
    authorization = base64_encode(f'waddle:{api_key}')

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {authorization}'
    }

    response = requests.request('POST', url, headers=headers, data=payload, allow_redirects=False)

    return json.loads(response.text)['access_token']


def send_sms(token, pn, message):
    url = 'https://sms.gabia.com/api/send/sms'
    payload = f'phone={pn}&callback=01096448928&message={message}&reqdate=0&refkey=[[RESTAPITEST1549847130]]'.encode("UTF-8")
    authorization = base64_encode(f'waddle:{token}')

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {authorization}'
    }

    response = requests.request('POST', url, headers=headers, data=payload, allow_redirects=False)

    return json.loads(response.text)['message']


def execute(sql, flag=False):
    with db.cursor() as cursor:
        cursor.execute(sql)
        if flag:
            result = cursor.fetchall()
            db.commit()
            return result
        db.commit()
        return None


def generate_code():
    return random.randrange(100000, 1000000)


def generate_token():
    token = ''

    while True:
        token = secrets.token_urlsafe(10)
        search = execute(f"""SELECT * FROM User WHERE Token='{token}';""", True)

        if len(search) == 0:
            break

    return token


def signup_request(P_PN, P_NAME):
    result = {}
    authcode = generate_code()

    try:
        execute(f"""DELETE FROM Sms WHERE PhoneNumber='{P_PN}' AND Name='{P_NAME}';""")
        execute(f"""INSERT INTO Sms (PhoneNumber, Name, Authcode) VALUES('{P_PN}', '{P_NAME}', {authcode});""")
        send_sms(get_token(), P_PN, f'인증번호 [{authcode}]를 입력해주세요.')
        result = {"result": "Success"}
    except:
        result = {"result": "Error"}

    return result


def signup_check(P_PN, P_NAME, P_AUTHCODE, ARN):
    result = {}

    try:
        execute(f"""DELETE FROM Sms WHERE SendTime <= DATE_SUB(NOW(), INTERVAL 30 MINUTE);""")
        
        search = execute(f"""SELECT Authcode, SendTime FROM Sms WHERE PhoneNumber='{P_PN}' AND Name='{P_NAME}';""", True)[0]

        authcode = search[0]
        sendtime = search[1]

        now = datetime.datetime.utcnow()

        delta = (now - sendtime).total_seconds()

        if delta <= 180 and int(P_AUTHCODE) == authcode:
            token = generate_token()
            execute(f"""DELETE FROM Sms WHERE PhoneNumber='{P_PN}' AND Name='{P_NAME}';""")
            execute(f"""UPDATE User SET PhoneNumber='01000000000' WHERE PhoneNumber='{P_PN}';""")
            execute(f"""INSERT INTO User (PhoneNumber, Name, Token, ARN) VALUES ('{P_PN}', '{P_NAME}', '{token}', '{ARN}');""")
            result = {"result": "Success", "token": token}
        elif delta <= 180:
            result = {"result": "Authcode Error"}
        else:
            result = {"result": "Timeout"}
        
    except:
        result = {"result": "Error"}

    return result


def login(P_TOKEN):
    result = {}

    try:
        search = execute(f"""SELECT PhoneNumber, Name FROM User WHERE Token='{P_TOKEN}';""", True)
        
        if len(search) == 0:
            return {"result": "No Such Token"}

        pn = search[0][0]
        name = search[0][1]

        result = {"result": "Success", "pn": pn, "name": name}

    except:
        result = {"result": "Error"}

    return result


def change_pn_request(P_TOKEN, P_PN):
    
    authcode = generate_code()

    try:
        search = execute(f"""SELECT PhoneNumber, Name FROM User WHERE Token='{P_TOKEN}';""", True)
        if len(search) == 0:
            return {"result": "No Such User"}
            
        P_PN_PREV = search[0][0]
        P_NAME = search[0][1]
            
        execute(f"""DELETE FROM Sms WHERE PhoneNumber='{P_PN_PREV}' AND Name='{P_NAME}';""")
        execute(f"""DELETE FROM Sms WHERE PhoneNumber='{P_PN}' AND Name='{P_NAME}';""")
        execute(f"""INSERT INTO Sms (PhoneNumber, Name, Authcode) VALUES('{P_PN}', '{P_NAME}', {authcode});""")
        send_sms(get_token(), P_PN, f'인증번호 [{authcode}]를 입력해주세요.')
        result = {"result": "Success"}
    except:
        result = {"result": "Error"}

    return result


def change_pn_check(P_TOKEN, P_PN, P_AUTHCODE):
    
    try:
        search = execute(f"""SELECT Name FROM User WHERE Token='{P_TOKEN}';""", True)
        if len(search) == 0:
            return {"result": "No Such User"}
            
        P_NAME = search[0][0]
        
        search = execute(f"""SELECT Authcode, SendTime FROM Sms WHERE PhoneNumber='{P_PN}' AND Name='{P_NAME}';""", True)[0]
        authcode = search[0]
        sendtime = search[1]

        now = datetime.datetime.utcnow()

        delta = (now - sendtime).total_seconds()

        if delta <= 180 and int(P_AUTHCODE) == authcode:
            execute(f"""DELETE FROM Sms WHERE PhoneNumber='{P_PN}' AND Name='{P_NAME}';""")
            execute(f"""UPDATE User SET PhoneNumber='{P_PN}' WHERE Token='{P_TOKEN}' AND Name='{P_NAME}';""")
            result = {"result": "Success"}
        else:
            result = {"result": "Timeout"}
    except:
        result = {"result": "Error"}
        
    return result
    

def change_name(P_TOKEN, P_NAME):
    try:
        search = execute(f"""SELECT * FROM User WHERE Token='{P_TOKEN}';""", True)
        if len(search) == 0:
            return {"result": "No Such User"}

        execute(f"""UPDATE User SET Name='{P_NAME}' WHERE Token='{P_TOKEN}'""")
        result = {"result": "Success"}
    except:
        result = {"result": "Error"}
    
    return result
    

def check_update(P_VERSION):
    if P_VERSION == '1.0.0':
        return "Success"
    else:
        return "Need Update"

    
def lambda_handler(event, context):
    global db
    P_PARAMS = event['params']
    P_QS = P_PARAMS['querystring']
    P_HEADER = P_PARAMS['header']

    result = None

    try:
        db = pymysql.connect(host=os.environ['DB_Host'],
                            port=3306,
                            user='admin',
                            passwd=os.environ['DB_Passwd'],
                            db='User2',
                            charset='utf8')

        P_FLAG = P_QS['flag']

        if P_FLAG == 'signup_request':
            result = signup_request(P_QS['pn'], P_QS['name'])
            pass
        elif P_FLAG == 'signup_check':
            result = signup_check(P_QS['pn'], P_QS['name'], P_QS['authcode'], P_QS['ARN'])
            pass
        elif P_FLAG == 'login':
            result = login(P_HEADER['token'])
            pass
        elif P_FLAG == 'change_pn_request':
            result = change_pn_request(P_HEADER['token'], P_QS['pn'])
            pass
        elif P_FLAG == 'change_pn_check':
            result = change_pn_check(P_HEADER['token'], P_QS['pn'], P_QS['authcode'])
            pass
        elif P_FLAG == 'change_name':
            result = change_name(P_HEADER['token'], P_QS['name'])
            pass
        elif P_FLAG == 'check_update':
            result = check_update(P_QS['version'])
            pass
        else:
            result = {"result": "Undefined flag"}
            pass

        db.close()
    except:
        result = {"result": "Unknown Error"}
    finally:
        pass

    return result


if __name__ == '__main__':
    pass
    # print(lambda_handler({'params':{'querystring':{'flag':'signup'}}}, None))