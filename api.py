import datetime
import json
from urllib import parse
import requests
import asyncio
import websockets


# 공공데이터 포털 단기예보 API
# 서비스 키와 URL
service_key = "BLWS9PdbSrtSL0vf%2BjBIADd695SRxWjNhtTja27KMP6oBdZRsnODs%2BeNaJSFJmvn1h7eGvbm8Vp64ftV552yMw%3D%3D"
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
print(url + param)  # API url을 출력합니다. 클릭하면 바로 웹페이지로 실행됩니다.
# JSON 파일을 제대로 보려면 크롬 JSON 뷰어 확장프로그램 설치가 필요합니다.

jsonObject = json.loads(response.text)
send_data = jsonObject.get("response").get("body").get("items").get("item")
JSONsting = json.dumps(send_data)


async def connect():
    async with websockets.connect("ws://localhost:9998/websocket") as websocket:
        await websocket.send(JSONsting);
        print("Data send completed");

# 비동기로 서버에 접속한다.
asyncio.get_event_loop().run_until_complete(connect())