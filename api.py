import datetime
import json
from urllib import parse

import requests


service_key = "BLWS9PdbSrtSL0vf%2BjBIADd695SRxWjNhtTja27KMP6oBdZRsnODs%2BeNaJSFJmvn1h7eGvbm8Vp64ftV552yMw%3D%3D"
url = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"



today = datetime.datetime.today()


param = f'?serviceKey={service_key}&' + parse.urlencode({
    parse.quote_plus('pageNo') : '1',
    parse.quote_plus('numOfRows') : '1000',
    parse.quote_plus('dataType') : 'JSON',
    parse.quote_plus('base_date') : today.strftime("%Y%m%d"),
    parse.quote_plus('base_time') : '0700',
    parse.quote_plus('nx') : '59',
    parse.quote_plus('ny') : '126'
})

response = requests.get(url+param)
print(url+param)
result = response.text
jsonObject = json.loads(result)
print(jsonObject.get("response").get("body").get("items").get("item"))