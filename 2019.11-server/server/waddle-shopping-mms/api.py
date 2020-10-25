# # key 발급
# import requests
# url = 'https://sms.gabia.com/oauth/token'
# payload = 'grant_type=client_credentials'
# headers = {
# 'Content-Type': 'application/x-www-form-urlencoded',
# 'Authorization': 'Basic d2FkZGxlOjBkNDE2ZTU3NDYzMTI5MWE4MGZlMzRhYThlMjc2MWE2'
# }
# response = requests.request('POST', url, headers = headers, data = payload, allow_redirects=False)
# print(response.text)

# 문자 보내기
import requests
url = 'https://sms.gabia.com/api/send/sms'
payload = 'phone=phone&callback=phone&message=SMS TEST MESSAGE&reqdate=0&refkey=key'
headers = { 
'Content-Type': 'application/x-www-form-urlencoded',
'Authorization': 'Basic key'
}
response = requests.request('POST', url, headers = headers, data = payload, allow_redirects=False)
print(response.text)