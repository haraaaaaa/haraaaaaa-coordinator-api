import datetime
import json
from urllib import parse
import requests
import asyncio
import websockets


# 공공데이터 포털 단기예보 API
# 서비스 키와 URL
service_key = "---"
url = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"

# API에서 당일 예보를 가져오기 위해 오늘 날짜를 변수에 선언하였습니다.
today = datetime.datetime.today()

# API를 호출하기 위한 param 값을 호출합니다. 주요 변수들은 아래와 같습니다.
param = f'?serviceKey={service_key}&' + parse.urlencode({
    parse.quote_plus('pageNo') : '1',
    parse.quote_plus('numOfRows') : '1000',
    parse.quote_plus('dataType') : 'JSON',
    parse.quote_plus('base_date') : today.strftime("%Y%m%d"),
    parse.quote_plus('base_time') : '0700',
    parse.quote_plus('nx') : '59',  # 원하는 위치의 X, Y 좌표 값입니다. 서울시 마포구 도화동으로 설정하였습니다.
    parse.quote_plus('ny') : '126'  # nx, ny 값에 따라 지역이 바뀝니다.
})

response = requests.get(url + param)

jsonObject = json.loads(response.text)
send_data = jsonObject.get("response").get("body").get("items").get("item")
JSONsting = json.dumps(send_data)


async def accept(websocket, path):
    getRequest = await websocket.recv(); # 프로세스 서버로부터 getRequest를 받습니다. getRequst를 따로 사용하진 않았습니다.
    print("GET Request Received"); # 정상적으로 요청을 받았음을 출력합니다.
    await websocket.send(JSONsting); # 요청을 받았으니 다시 JSON 데이터를 송부합니다.
    print("JSON data Successfully Sent"); # 정상적으로 JSON 파일을 보냈음을 출력합니다.

start_server = websockets.serve(accept, "localhost", 9998); # localhost 9998번 포트를 통해 통신을 합니다.

loop = asyncio.get_event_loop()
loop.run_until_complete(start_server);
loop.run_forever();

