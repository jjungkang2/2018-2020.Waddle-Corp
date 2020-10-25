import pymysql
import os
import json
import boto3

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


# get_destination: token을 가진 유저의 배송지 정보를 추가된 순서대로 보내준다.
def get_dest(P_TOKEN):
    try:
        search = execute(f"""SELECT * FROM User WHERE Token='{P_TOKEN}';""", True)
        
        if len(search) == 0:
            return {"result": "No Such User"}
    
        dest = execute(f"""SELECT DestName, Destination FROM Destination WHERE Token='{P_TOKEN}' ORDER BY TimeStamp;""", True)
    
        if len(dest) == 0:
            return {"result": "No Destination"}
        
        dest_list = [{'name': x[0], 'destination': x[1]} for x in dest]
        return_str={}
        return_str["result"] = "Success"
        return_str["list"] = dest_list
    except:
        return_str={"result": "Error"}

    return return_str


def add_dest(P_TOKEN, P_DESTNAME, P_DESTINATION):
    try:
        search = execute(f"""SELECT * FROM User WHERE Token='{P_TOKEN}';""", True)
    
        if len(search) == 0:
            return {"result": "No Such User"}
    
        # Check the list has already 5 destinations
        search = execute(f"""SELECT * FROM Destination WHERE Token='{P_TOKEN}';""", True)
    
        if len(search) >= 5:
            return {"result": "Already 5 Destinations"}
    
        search = execute(f"""SELECT * FROM Destination WHERE Token='{P_TOKEN}' AND DestName='{P_DESTNAME}';""", True)
    
        if len(search) == 0:
            execute(f"""INSERT INTO Destination (Token, DestName, Destination) VALUES('{P_TOKEN}', '{P_DESTNAME}', '{P_DESTINATION}');""")
            result = {"result": "Success"}
        else:
            result = {"result": "Existing DestName"}
    except:
        result = {"result": "Error"}
        
    return result
    

def update_dest_name(P_TOKEN, P_DESTNAME_PREV, P_DESTNAME):
    try:
        search = execute(f"""SELECT * FROM User WHERE Token='{P_TOKEN}';""", True)
    
        if len(search) == 0:
            return {"result": "No Such User"}
            
        search = execute(f"""SELECT * FROM Destination WHERE Token='{P_TOKEN}' AND DestName='{P_DESTNAME_PREV}';""", True)
        
        if len(search) == 0:
            return {"result": "No Such DestName"}
            
        search = execute(f"""SELECT * FROM Destination WHERE Token='{P_TOKEN}' AND DestName='{P_DESTNAME}';""", True)
        
        if len(search) >= 1:
            return {"result": "Existing DestName"}
            
        execute(f"""UPDATE Destination SET DestName='{P_DESTNAME}' WHERE Token='{P_TOKEN}' AND DestName='{P_DESTNAME_PREV}';""")
        result = {"result": "Success"}
    except:
        result = {"result": "Error"}
        
    return result

def update_dest_dest(P_TOKEN, P_DESTNAME, P_DESTINATION):
    try:
        search = execute(f"""SELECT * FROM User WHERE Token='{P_TOKEN}';""", True)
        
        if len(search) == 0:
            return {"result": "No Such User"}
            
        search = execute(f"""SELECT * FROM Destination WHERE Token='{P_TOKEN}' AND DestName='{P_DESTNAME}';""", True)
        
        if len(search) == 0:
            return {"result": "No Such DestName"}
        
        execute(f"""UPDATE Destination SET Destination='{P_DESTINATION}' WHERE Token='{P_TOKEN}' AND DestName='{P_DESTNAME}';""")
        result = {"result": "Success"}
    except:
        result = {"result": "Error"}
        
    return result
    

def delete_dest(P_TOKEN, P_DESTNAME):
    try:
        search = execute(f"""SELECT * FROM User WHERE Token='{P_TOKEN}';""", True)
        
        if len(search) == 0:
            return {"result": "No Such User"}
            
        search = execute(f"""SELECT * FROM Destination WHERE Token='{P_TOKEN}' AND DestName='{P_DESTNAME}';""", True)
        
        if len(search) == 0:
            return {"result": "No Such DestName"}
        
        execute(f"""DELETE FROM Destination WHERE Token='{P_TOKEN}' AND DestName='{P_DESTNAME}';""")
        result = {"result": "Success"}
    except:
        result = {"result": "Error"}
        
    return result


def get_basket(P_TOKEN):
    try:
        result = {}
        search = execute(f"""SELECT * FROM User WHERE Token='{P_TOKEN}';""", True)
        
        if len(search) == 0:
            return {"result": "No Such User"}
            
        basket = execute(f"""SELECT ProductID, ProductOption, ProductCount FROM Basket WHERE Token='{P_TOKEN}' ORDER BY TimeStamp DESC;""", True)
        
        if len(basket) == 0:
            return {"result": "No Products"}
            
        basket_list = [{'id':str(x[0]), 'option':x[1], 'count': str(x[2])} for x in basket]
        result['result'] = 'Success'
        result['list'] = basket_list
    except:
        result['result'] = "Error"
    
    return result


def add_basket(P_TOKEN, P_ID, P_OPTION, P_COUNT):
    try:
        search = execute(f"""SELECT * FROM User WHERE Token='{P_TOKEN}';""", True)
        
        if len(search) == 0:
            return {"result": "No Such User"}
            
        basket = execute(f"""SELECT * FROM Basket WHERE Token='{P_TOKEN}';""", True)
        
        if len(basket) >= 100:
            return {"result": "Already 100 products"}
    
        avail = execute(f"""SELECT ProductCount FROM Basket WHERE Token='{P_TOKEN}' AND ProductID={P_ID} AND ProductOption='{P_OPTION}';""", True)
    
        if len(avail) == 0:
            execute(f"""INSERT INTO Basket (Token, ProductId, ProductOption, ProductCount) VALUES('{P_TOKEN}', {P_ID}, '{P_OPTION}', {P_COUNT});""")
        else:
            avail_count = avail[0][0]
            execute(f"""UPDATE Basket SET ProductCount={avail_count+int(P_COUNT)} WHERE Token='{P_TOKEN}' AND ProductID={P_ID} AND ProductOption='{P_OPTION}';""")
            
        result = {"result": "Success"}
    except:
        result = {"result": "Error"}
        
    return result
    

def update_basket(P_TOKEN, P_ID, P_OPTION_PREV, P_COUNT_PREV, P_OPTION, P_COUNT):
    try:
        search = execute(f"""SELECT * FROM User WHERE Token='{P_TOKEN}';""", True)
        
        if len(search) == 0:
            return {"result": "No Such User"}
    
        basket = execute(f"""SELECT ProductOption, ProductCount FROM Basket WHERE Token='{P_TOKEN}' AND ProductID={P_ID} AND ProductOption='{P_OPTION_PREV}' AND ProductCount={P_COUNT_PREV};""", True)
    
        if len(basket) == 0:
            return {"result": "No Such Product"}
        else:
            execute(f"""UPDATE Basket SET ProductOption='{P_OPTION}', ProductCount={P_COUNT} WHERE Token='{P_TOKEN}' AND ProductID={P_ID} AND ProductOption='{P_OPTION_PREV}' AND ProductCount={P_COUNT_PREV};""")
            
        result = {"result": "Success"}
    except:
        result = {"result": "Error"}
        
    return result
    

def delete_basket(P_TOKEN, P_ID, P_OPTION, P_COUNT):
    try:
        search = execute(f"""SELECT * FROM User WHERE Token='{P_TOKEN}';""", True)
        
        if len(search) == 0:
            return {"result": "No Such User"}
    
        basket = execute(f"""SELECT ProductOption, ProductCount FROM Basket WHERE Token='{P_TOKEN}' AND ProductID={P_ID} AND ProductOption='{P_OPTION}' AND ProductCount={P_COUNT};""", True)
    
        if len(basket) == 0:
            return {"result": "No Such Product"}
        else:
            execute(f"""DELETE FROM Basket WHERE Token='{P_TOKEN}' AND ProductID={P_ID} AND ProductOption='{P_OPTION}' AND ProductCount={P_COUNT};""")
            
        result = {"result": "Success"}
    except:
        result = {"result": "Error"}
    
    return result

def get_ordered(P_TOKEN):
    try:
        result = {}
        search = execute(f"""SELECT * FROM User WHERE Token='{P_TOKEN}';""", True)
        
        if len(search) == 0:
            return {"result": "No Such User"}
            
        ordered = execute(f"""SELECT * FROM Ordered WHERE Token='{P_TOKEN}';""", True)
        
        if len(ordered) == 0:
            return {"result": "No Ordered"}
        else:
            ordered_list = [{'id':str(x[1]), 'name':x[2], 'option':x[3], 'count':x[5], 'price': x[6], 'destination': x[7], 'orderid':str(x[8]), 'deliverydate':x[9], 'status':x[10]} for x in ordered]
            result['result'] = "Success"
            result['list'] = ordered_list
    except:
        result = {"result": "Error"}
        
    return result
    

def get_ordered_product(P_TOKEN, P_ORDER_ID, P_ID, P_OPTION):
    try:
        result = {}
        search = execute(f"""SELECT * FROM User WHERE Token='{P_TOKEN}';""", True)
        
        if len(search) == 0:
            return {"result": "No Such User"}
            
        ordered = execute(f"""SELECT * FROM Ordered WHERE Token='{P_TOKEN}' AND ProductID={P_ID} AND ProductOption='{P_OPTION}' AND OrderID='{P_ORDER_ID}';""", True)
        
        if len(ordered) == 0:
            return {"result": "No Ordered"}
        else:
            ordered_list = [{'id':str(x[1]), 'name':x[2], 'option':x[3], 'count':x[5], 'price': x[6], 'destination': x[7], 'orderid':str(x[8]), 'deliverydate':x[9], 'status':x[10]} for x in ordered]
            result['result'] = "Success"
            result['list'] = ordered_list
    except:
        result = {"result": "Error"}
    
    return result
    

def get_price(P_TOKEN, P_PRICE):
    try:
        result = {}
        search = execute(f"""SELECT * FROM User WHERE Token='{P_TOKEN}';""", True)
        
        if len(search) == 0:
            return {"result": "No Such User"}
            
        while(True):
            price = execute(f"""SELECT * FROM Ordered WHERE ProductPrice='{P_PRICE}';""", True)
            
            if len(price) != 0:
                P_PRICE = str(int(P_PRICE)+100)
            else:
                break
        
        result['result'] = "Success"
        result['price'] = P_PRICE
    except:
        result = {"result": "Error"}
        
    return result
        


def add_ordered(P_TOKEN, P_ID, P_NAME, P_OPTION, P_OPTIONID, P_COUNT, P_PRICE, P_DESTINATION):
    try:
        search = execute(f"""SELECT * FROM User WHERE Token='{P_TOKEN}';""", True)
        
        if len(search) == 0:
            return {"result": "No Such User"}
            
        execute(f"""INSERT INTO Ordered (Token, ProductID, ProductName, ProductOption, ProductOptionID, ProductCount, ProductPrice, Destination, Status) VALUES('{P_TOKEN}', {P_ID}, {P_NAME}, '{P_OPTION}', '{P_OPTIONID}', {P_COUNT}, '{P_PRICE}', '{P_DESTINATION}', 'payment request');""")
        execute(f"""DELETE FROM Basket WHERE Token='{P_TOKEN}' AND ProductID={P_ID} AND ProductOption='{P_OPTION}' AND ProductCount={P_COUNT};""")
        result = {"result": "Success"}
    except:
        result = {"result": "Error"}
        
    return result


def delete_ordered(P_TOKEN, P_ID, P_OPTION, P_COUNT):
    try:
        search = execute(f"""SELECT * FROM User WHERE Token='{P_TOKEN}';""", True)
        
        if len(search) == 0:
            return {"result": "No Such User"}
            
        order = execute(f"""SELECT * FROM Ordered WHERE Token='{P_TOKEN}' AND ProductID={P_ID} AND ProductOption='{P_OPTION}' AND ProductCount={P_COUNT};""", True)
        if len(order) == 0:
            return {"result": "No Such Order"}
        
        execute(f"""DELETE FROM Ordered WHERE Token='{P_TOKEN}' AND ProductID={P_ID} AND ProductOption='{P_OPTION}' AND ProductCount={P_COUNT};""")
        result = {"result": "Success"}
    except:
        result = {"result": "Error"}
        
    return result


# def get_point(name, pn):
#     search = execute(f"""SELECT Point FROM User WHERE Name='{name}' AND PhoneNumber='{pn}';""", True)

#     if len(search) == 0:
#         return 'Error:No Such User'

#     Point = search[0][0]
#     return 'Success:' + str(Point)


# def set_point(name, pn, point):
#     search = execute(f"""SELECT Point FROM User WHERE Name='{name}' AND PhoneNumber='{pn}';""", True)

#     if len(search) == 0:
#         return 'Error:No Such User'
    
#     nowpoint = search[0][0]
#     execute(f"""UPDATE User SET Point={point} WHERE Name='{name}' AND PhoneNumber='{pn}';""")
#     return 'Success:' + point


# def add_point(name, pn, point):
#     search = execute(f"""SELECT Point FROM User WHERE Name='{name}' AND PhoneNumber='{pn}';""", True)

#     if len(search) == 0:
#         return 'Error:No Such User'
    
#     nowpoint = search[0][0]
#     execute(f"""UPDATE User SET Point={nowpoint+int(point)} WHERE Name='{name}' AND PhoneNumber='{pn}';""")
#     return 'Success:' + str(nowpoint+int(point))


# def sub_point(name, pn, point):
#     search = execute(f"""SELECT Point FROM User WHERE Name='{name}' AND PhoneNumber='{pn}';""", True)

#     if len(search) == 0:
#         return 'Error:No Such User'
    
#     nowpoint = search[0][0]
#     execute(f"""UPDATE User SET Point={nowpoint-int(point)} WHERE Name='{name}' AND PhoneNumber='{pn}';""")
#     return 'Success:' + str(nowpoint-int(point))


def add_exchange(P_TOKEN, P_ID, P_OPTION, P_COUNT, P_ORDER_ID, P_REASON, P_DETAIL, P_DESTINATION, P_REQUESTS):    
    try:
        search = execute(f"""SELECT * FROM User WHERE Token='{P_TOKEN}';""", True)
        
        if len(search) == 0:
            return {"result": "No Such User"}
            
        order = execute(f"""SELECT * FROM Ordered WHERE Token='{P_TOKEN}' AND ProductID={P_ID} AND ProductOption='{P_OPTION}';""", True)
        if len(order) == 0:
            return {"result": "No Such Order"}
        
        order = execute(f"""SELECT * FROM Ordered WHERE Token='{P_TOKEN}' AND ProductID={P_ID} AND ProductOption='{P_OPTION}' AND (Status='delivered' OR Status='exchanged');""", True)
        if len(order) == 0:
            return {"result": "No Delivered"}
            
        x = order[0]
        execute(f"""INSERT INTO ExchangeRefund (Token, ProductID, ProductName, ProductOption, ProductOptionID, ProductCount, ProductPrice, OrderID, Reason, Detail, Destination, Request, Status) VALUES('{x[0]}', {x[1]}, '{x[2]}', '{x[3]}', {x[4]}, {x[5]}, {x[6]}, '{x[8]}', '{P_REASON}', '{P_DETAIL}', '{P_DESTINATION}', '{P_REQUESTS}', 'exchange request in');""")
        execute(f"""UPDATE Ordered SET Status='exchange request in' WHERE Token='{P_TOKEN}' AND ProductID={P_ID} AND ProductOption='{P_OPTION}' AND (Status='delivered' OR Status='exchanged');""")
        
        result = {"result": "Success"}
    except:
        result = {"result": "Error"}
        
    return result


def add_refund(P_TOKEN, P_ID, P_OPTION, P_COUNT, P_ORDER_ID, P_REASON, P_DETAIL, P_DESTINATION, P_REQUESTS):
    try:
        search = execute(f"""SELECT * FROM User WHERE Token='{P_TOKEN}';""", True)
        
        if len(search) == 0:
            return {"result": "No Such User"}
            
        order = execute(f"""SELECT * FROM Ordered WHERE Token='{P_TOKEN}' AND ProductID={P_ID} AND ProductOption='{P_OPTION}' AND ProductCount={P_COUNT};""", True)
        if len(order) == 0:
            return {"result": "No Such Order"}
        
        order = execute(f"""SELECT * FROM Ordered WHERE Token='{P_TOKEN}' AND ProductID={P_ID} AND ProductOption='{P_OPTION}' AND ProductCount={P_COUNT} AND (Status='delivered' OR Status='exchanged');""", True)
        if len(order) == 0:
            return {"result": "No Delivered"}
        
        x = order[0]
        execute(f"""INSERT INTO ExchangeRefund (Token, ProductID, ProductName, ProductOption, ProductOptionID, ProductCount, ProductPrice, OrderID, Reason, Detail, Destination, Request, Status) VALUES('{x[0]}', {x[1]}, '{x[2]}', '{x[3]}', {x[4]}, {x[5]}, {x[6]}, '{x[8]}', '{P_REASON}', '{P_DETAIL}', '{P_DESTINATION}', '{P_REQUESTS}', 'refund request in');""")
        execute(f"""UPDATE Ordered SET Status='refund request in' WHERE Token='{P_TOKEN}' AND ProductID={P_ID} AND ProductOption='{P_OPTION}' AND ProductCount={P_COUNT} AND (Status='delivered' OR Status='exchanged');""")
        
        result = {"result": "Success"}
    except:
        result = {"result": "Error"}
        
    return result
    

def add_confirmed(P_TOKEN, P_ORDER_ID):
    try:
        search = execute(f"""SELECT * FROM User WHERE Token='{P_TOKEN}';""", True)
        
        if len(search) == 0:
            return {"result": "No Such User"}
            
        order = execute(f"""SELECT * FROM Ordered WHERE Token='{P_TOKEN}' AND OrderID={P_ORDER_ID};""", True)
        if len(order) == 0:
            return {"result": "No Such Order"}
        
        order = execute(f"""SELECT * FROM Ordered WHERE Token='{P_TOKEN}' AND OrderID={P_ORDER_ID} AND (Status='delivered' OR Status='exchanged' OR Status='exchange disallowed' OR Status='refund disallowed');""", True)
        if len(order) == 0:
            return {"result": "No Delivered"}
        
        x = order[0]
        execute(f"""UPDATE Ordered SET Status='confirmed' WHERE Token='{P_TOKEN}' AND OrderID={P_ORDER_ID} AND (Status='delivered' OR Status='exchanged' OR Status='exchange disallowed' OR Status='refund disallowed');""")
        
        result = {"result": "Success"}
    except:
        result = {"result": "Error"}
        
    return result
    

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

        if P_FLAG == 'get_dest':
            result = get_dest(P_HEADER['token'])
            pass
        elif P_FLAG == 'add_dest':
            result = add_dest(P_HEADER['token'], P_QS['name'], P_QS['dest'])
            pass
        elif P_FLAG == 'update_dest_name':
            result = update_dest_name(P_HEADER['token'], P_QS['pname'], P_QS['fname'])
            pass
        elif P_FLAG == 'update_dest_dest':
            result = update_dest_dest(P_HEADER['token'], P_QS['name'], P_QS['dest'])
            pass
        elif P_FLAG == 'delete_dest':
            result = delete_dest(P_HEADER['token'], P_QS['name'])
            pass
        elif P_FLAG == 'get_basket':
            result = get_basket(P_HEADER['token'])
            pass
        elif P_FLAG == 'add_basket':
            result = add_basket(P_HEADER['token'], P_QS['id'], P_QS['option'], P_QS['count'])
            pass
        elif P_FLAG == 'update_basket':
            result = update_basket(P_HEADER['token'], P_QS['id'], P_QS['poption'], P_QS['pcount'], P_QS['foption'], P_QS['fcount'])
            pass
        elif P_FLAG == 'delete_basket':
            result = delete_basket(P_HEADER['token'], P_QS['id'], P_QS['option'], P_QS['count'])
            pass
        elif P_FLAG == 'get_ordered':
            result = get_ordered(P_HEADER['token'])
            pass
        elif P_FLAG == 'get_ordered_product':
            result = get_ordered_product(P_HEADER['token'], P_QS['orderid'], P_QS['pid'], P_QS['poption'])
            pass
        elif P_FLAG == 'get_price':
            result = get_price(P_HEADER['token'], P_QS['price'])
        elif P_FLAG == 'add_ordered':
            result = add_ordered(P_HEADER['token'], P_QS['id'], P_QS['name'], P_QS['option'], P_QS['optionid'], P_QS['count'], P_QS['price'], P_QS['destination'])
            pass
        elif P_FLAG == 'delete_ordered':
            result = delete_ordered(P_HEADER['token'], P_QS['id'], P_QS['option'], P_QS['count'])
            pass
        elif P_FLAG == 'add_exchange':
            result = add_exchange(P_HEADER['token'], P_QS['pid'], P_QS['poption'], P_QS['pcount'], P_QS['porderid'], P_QS['reason'], P_QS['detail'], P_QS['pdestination'], P_QS['requests'])
            pass
        elif P_FLAG == 'add_refund':
            result = add_refund(P_HEADER['token'], P_QS['pid'], P_QS['poption'], P_QS['pcount'], P_QS['porderid'], P_QS['reason'], P_QS['detail'], P_QS['pdestination'], P_QS['requests'])
            pass
        elif P_FLAG == 'add_confirmed':
            result = add_confirmed(P_HEADER['token'], P_QS['porderid'])
        else:
            result = {"result": "Undefined flag"}
            pass

        db.close()
    finally:
        pass

    return result


if __name__ == '__main__':
    pass
    # print(lambda_handler({'params':{'querystring':{'flag':'get_destination', 'name':'장민성', 'pn':'01021431238'}}}, None))