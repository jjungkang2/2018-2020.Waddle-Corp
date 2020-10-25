import requests
import json     

headers = {
    'data' : 'currentPage=1&countPerPage=10&resultType=json&confmKey=key&keyword=keyword',
    'dataType' : 'jsonp',
    'crossDomain' : 'True'}

req = requests.get('http://www.juso.go.kr/addrlink/addrLinkApiJsonp.do', headers = headers) 

if req.status_code == requests.codes.ok:    
    print("접속 성공")
    stock_data = json.loads(req.text)
else:
    print("접속 실패")