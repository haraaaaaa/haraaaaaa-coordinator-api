import json
from flask import request
from flask import jsonify
from . import api
import datetime
from pytz import timezone
import requests
from urllib import parse

Weather_api_key = "---"                                                               #
Weather_url = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"

@api.route('/weather',methods=['GET'])
def weather():
    if request.method=='GET':
        today = datetime.datetime.now(timezone('Asia/Seoul'))
        hour,minute = str(today.hour),'30' if today.minute>30 else '00'
        print(today)
        param = f'?serviceKey={Weather_api_key}&' + parse.urlencode({
        parse.quote_plus('pageNo') : '1',
        parse.quote_plus('numOfRows') : '1000',
        parse.quote_plus('dataType') : 'JSON',
        parse.quote_plus('base_date') : today.strftime("%Y%m%d"),
        parse.quote_plus('base_time') : hour+minute,
        parse.quote_plus('nx') : '59',  # 원하는 위치의 X, Y 좌표 값입니다. 서울시 마포구 도화동으로 설정하였습니다.
        parse.quote_plus('ny') : '126'  # nx, ny 값에 따라 지역이 바뀝니다.
        })
        content = requests.get(Weather_url + param)

        jsonObject = content.json()#json.loads(content.text)
        send_data = jsonObject.get("response").get("body").get("items").get("item")
        print(send_data)
        JSONstring = json.dumps(send_data)
        return jsonify(send_data)
    
# @api.route('/slack',methods=['GET','POST'])
# def slack():
#     if request.method=='POST':
#         res = requests.post('webhook url',
#         json={}, headers={'Content-Type':'application/json'})

#     elif request.method == 'GET':
#         pass

#     data = request.get_json()
#     return jsonify(data)

# @api.route('/resend',methods=['GET'])
# def resend():
#     res = requests.get('https://nomer26.pythonanywhere.com/api/v1/weather')
#     res = res.json()
#     return jsonify(res)
