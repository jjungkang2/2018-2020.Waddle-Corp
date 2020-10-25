import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

requests.post(
    'http://www.juso.go.kr/addrlink/addrMobileLinkUrl.do%22;',
    files=(
        ('confmKey', 'key'),
        ('returnUrl', 'waddlelab.com'),
        ('resultType', 4)
    )
)