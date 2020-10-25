import pymysql
import os
import random

import json
import requests
import base64


db = None

# Execute SQL Query
def execute(sql, flag=False):
    with db.cursor() as cursor:
        cursor.execute(sql)
        if flag:
            result = cursor.fetchall()
            db.commit()
            return result
        db.commit()
        return None

def ordered_push(name):
    return name

def get_next_id():
    max_id = execute("""SELECT MAX(Id) FROM User""", True)[0][0]

    if max_id == None:
        return 1
    else:
        return max_id+1
    

# signup_request_sms : Request for SMS Authentication Code
def signup_request_sms(name, pn):
    return_str = ''
    search = execute(f"""SELECT * FROM User WHERE Name='{name}' AND PhoneNumber='{pn}';""", True)

    if len(search) > 0:
        return_str = 'Error:Duplicated User'
    else:
        authcode = generate_code()
        execute(f"""DELETE FROM Sms WHERE Name='{name}' AND PhoneNumber='{pn}';""")
        execute(f"""INSERT INTO Sms VALUES('{name}', '{pn}', {authcode});""")
        send_sms(get_token(), pn, f'인증번호 [{authcode}]를 입력해주세요.')
        return_str = 'Success'

    return return_str
    


# signup_check_code : Check Authentication Code
def signup_check_code(name, pn, pw, code, isblind):
    return_str = ''
    search = execute(f"""SELECT Authcode FROM Sms WHERE Name='{name}' AND PhoneNumber='{pn}';""", True)

    if len(search) == 0:
        return_str = 'Error:No Such User'
    
    authcode = search[0][0]
    
    if int(code) == authcode:
        execute(f"""DELETE FROM Sms WHERE Name='{name}' AND PhoneNumber='{pn}';""")
        execute(f"""INSERT INTO User VALUES('{name}', '{pn}', '{pw}', {get_next_id()}, 0, {isblind})""")
        return_str = 'Success'
    else:
        return_str = f'Error:Code are not same'

    return return_str


# Functions for Login scenario
# login_request : Request for Login, return such name if exist
def login_request(pn, pw):
    return_str = ''
    return_name = ''
    search = execute(f"""SELECT Name FROM User WHERE PhoneNumber='{pn}' AND Passwd='{pw}';""", True)

    if len(search) == 0:
        search_only_passwd = execute(f"""SELECT * FROM User WHERE Passwd='{pw}';""", True)
        search_only_pn = execute(f"""SELECT * FROM User WHERE PhoneNUmber='{pn}';""", True)
        if len(search_only_passwd) > 0 and len(search_only_pn) > 0:
            return_str = 'Error:Using passwd and pn'
        elif len(search_only_passwd) > 0:
            return_str = 'Error:Using passwd'
        elif len(search_only_pn) > 0:
            return_str = 'Error:Using pn'
        else:
            return_str = 'Error:No Such User'
    elif len(search) > 1:
        return_str = 'Error:Too Many Users'
    else:
        return_str = 'Success'
        return_name = search[0][0]

    if return_name == '':
        return {
            "result":return_str
        }
    else:
        return {
            "result":return_str,
            "name":return_name
        }


# Functions for Change PN scenario
# change_requst : Request for changing Phone Number
def change_request(name, ppn, fpn, pw):
    return_str = ''
    search = execute(f"""SELECT * FROM User WHERE Name='{name}' AND PhoneNumber='{ppn}' AND Passwd='{pw}';""", True)

    if len(search) == 0:
        return_str = 'Error:No Such User'
    else:
        authcode = generate_code()
        execute(f"""DELETE FROM Sms WHERE Name='{name}' AND PhoneNumber='{fpn}';""")
        execute(f"""INSERT INTO Sms VALUES('{name}', '{fpn}', {authcode});""")
        send_sms(get_token(), fpn, f'인증번호 [{authcode}]를 입력해주세요.')
        return_str = 'Success'

    return return_str


# change_check_code : Check Authentication Code
def change_check_code(name, ppn, fpn, pw, code):
    return_str = ''
    search = execute(f"""SELECT Authcode FROM Sms WHERE Name='{name}' AND PhoneNumber='{ppn}';""", True)

    if len(search) == 0:
        return_str = 'Error:No Such User'
    
    authcode = search[0][0]
    
    if int(code) == authcode:
        execute(f"""DELETE FROM Sms WHERE Name='{name}' AND PhoneNumber='{fpn}';""")
        execute(f"""UPDATE User SET PhoneNumber='{fpn}' WHERE Name='{name}' AND PhoneNumber='{ppn}' AND Passwd='{pw}';""")
        return_str = 'Success'
    else:
        return_str = 'Error:Code are not same'

    return return_str
    

# Functions for Finding PW scenario
# find_pw_request : Request for finding pw
def find_pw_request(name, pn):
    return_str = ''
    search = execute(f"""SELECT * FROM User WHERE Name='{name}' AND PhoneNumber='{pn}';""", True)

    if len(search) == 0:
        return_Str = 'Error:No Such User'
    else:
        authcode = generate_code()
        execute(f"""DELETE FROM Sms WHERE Name='{name}' AND PhoneNumber='{pn}';""")
        execute(f"""INSERT INTO Sms VALUES('{name}', '{pn}', {authcode});""")
        send_sms(get_token(), pn, f'인증번호 [{authcode}]를 입력해주세요.')
        return_str = 'Success'

    return return_str


# find_pw_check_code : Check Authentication Code
def find_pw_check_code(name, pn, code):
    return_str = ''
    search = execute(f"""SELECT Authcode FROM Sms WHERE Name='{name}' AND PhoneNumber='{pn}';""", True)

    if len(search) == 0:
        return_str = 'Error:No Such User'
    
    authcode = search[0][0]
    
    if int(code) == authcode:
        newpw = generate_passwd()
        execute(f"""DELETE FROM Sms WHERE Name='{name}' AND PhoneNumber='{pn}';""")
        execute(f"""UPDATE User SET Passwd='{newpw}' WHERE Name='{name}' AND PhoneNumber='{pn}';""")
        send_sms(get_token(), pn, f'임시 비밀번호는 [{newpw}]입니다.')
        return_str = 'Success'
    else:
        return_str = 'Error:Code are not same'

    return return_str


def change_name(pname, fname, pn, pw):
    return_str = ''
    search = execute(f"""SELECT * FROM User WHERE Name='{pname}' AND PhoneNumber='{pn}' AND Passwd='{pw}';""", True)

    if len(search) == 0:
        return_str = 'Error:No Such User'
    else:
        execute(f"""UPDATE User SET Name='{fname}' WHERE Name='{pname}' AND PhoneNumber='{pn}' AND Passwd='{pw}'""")
        return_str = 'Success'

    return return_str


def change_pn(name, ppn, fpn, pw):
    return_str = ''
    search = execute(f"""SELECT * FROM User WHERE Name='{name}' AND PhoneNumber='{ppn}' AND Passwd='{pw}';""", True)

    if len(search) == 0:
        return_str = 'Error:No Such User'
    else:
        execute(f"""UPDATE User SET PhoneNumber='{fpn}' WHERE Name='{name}' AND PhoneNumber='{ppn}' AND Passwd='{pw}'""")
        return_str = 'Success'

    return return_str


def change_passwd(name, pn, ppw, fpw):
    return_str = ''
    search = execute(f"""SELECT * FROM User WHERE Name='{name}' AND PhoneNumber='{pn}' AND Passwd='{ppw}';""", True)

    if len(search) == 0:
        return_str = 'Error:No Such User'
    else:
        execute(f"""UPDATE User SET Passwd='{fpw}' WHERE Name='{name}' AND PhoneNumber='{pn}' AND Passwd='{ppw}'""")
        return_str = 'Success'

    return return_str


def delete_user(name, pn, pw):
    return_str = ''
    search = execute(f"""SELECT Id FROM User WHERE Name='{name}' AND PhoneNumber='{pn}' AND Passwd='{pw}';""", True)

    if len(search) == 0:
        return_str = 'Error:No Such User'
    else:
        Id = search[0][0]
        execute(f"""DELETE FROM User WHERE Name='{name}' AND PhoneNumber='{pn}' AND Passwd='{pw}';""")
        execute(f"""DELETE FROM Basket WHERE Id={Id};""")
        return_str = 'Success'

    return return_str


# lambda handler
def lambda_handler(event, context):
    global db
    flag2 = False
    params = event['params']
    qs = params['querystring']
    result = ''

    try:
        db = pymysql.connect(host=os.environ['DB_Host'],
                            port=3306,
                            user='admin',
                            passwd=os.environ['DB_Passwd'],
                            db='User',
                            charset='utf8')

        flag = qs['flag']

        if flag == 'ordered_push':
            result == ordered_push(qs[''])
        elif flag == 'exchange_push':
            result == exchange_push(qs[''])
        elif flag == 'refund_push':
            result == refund_push(qs[''])
        else:
            result = 'Undefined flag'

        db.close()
    finally:
        pass

    if flag2 == True:
        str_return = result
    else:
        str_return = {'result': result}

    return str_return


if __name__ == '__main__':
    pass
    # print(lambda_handler({'params':{'querystring':{'flag':'signup'}}}, None))