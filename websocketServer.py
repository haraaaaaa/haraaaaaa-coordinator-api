###########
# Server
import datetime
import json
from urllib import parse
import requests
import asyncio
import websockets

## 나는 왜 클래스를 사용했을까.. GC가 있어도 일회성 객체인데 이게 나의 편의를 위해 효율을 버린것 같다. 생각없이 작성한것 같다..

# TC('Title') / SC('req','res') / returned ,

class API:
    def __init__(self,**kwargs):
        self.TC = kwargs['TC']
        self.SC = kwargs['SC']
        self.kwargs = kwargs
        self.returned = kwargs['returned']
        self.content = None
        self.response = None


    async def run(self):
        result = Title_Code[self.TC](**self.kwargs)
        Sub_Code = {'req':result.request,'res':result._response}
        self.SC = await Sub_Code[self.SC]()
        # add process
        if self.returned:
            self.response = await Sub_Code[self.SC]()
            return self.response


class Coordinate(API):  # 굳이 또 나눈 이유 : 에러 및 비동기로 더 빠르게 처리하기 위해

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.endpoint = None
        if self.TC !='Coordinate':return {} # error

    async def request(self):   # API 요청 쿼리 생성
        if self.TC !='Coordinate' or self.SC !='req':return {} # error

        # API에서 당일 예보를 가져오기 위해 오늘 날짜를 변수에 선언하였습니다.
        today = datetime.datetime.today()

        # API를 호출하기 위한 param 값을 호출합니다. 주요 변수들은 아래와 같습니다.
        param = f'?serviceKey={Weather_api_key}&' + parse.urlencode({
            parse.quote_plus('pageNo') : '1',
            parse.quote_plus('numOfRows') : '1000',
            parse.quote_plus('dataType') : 'JSON',
            parse.quote_plus('base_date') : today.strftime("%Y%m%d"),
            parse.quote_plus('base_time') : '0700',
            parse.quote_plus('nx') : '59',  # 원하는 위치의 X, Y 좌표 값입니다. 서울시 마포구 도화동으로 설정하였습니다.
            parse.quote_plus('ny') : '126'  # nx, ny 값에 따라 지역이 바뀝니다.
        })
        self.endpoint = param  ###
        self.SC = 'res'
        return self.SC

    async def _response(self):  # 요청 및 필수요소 추출 후 다시 클라이언트에 전송
        if self.endpoint is None: return {} # error
        content = requests.get(Weather_url + self.endpoint)
        jsonObject = json.loads(content.text)
        send_data = jsonObject.get("response").get("body").get("items").get("item")
        JSONstring = json.dumps(send_data)
        self.response = {'JSON':JSONstring,'TC':'Coordinate','SC':'res'}  ## 클라이언트가 받는
        return self.response


async def process(websocket, path):
    items = await websocket.recv()
    items = json.loads(items)
    api = API(**items)
    await api.run()
    if api.returned:
        items = json.dumps(api.response)

        await websocket.send(items)  
        print(f"> Complete Submit")


if __name__=='__main__': 
    
    ####################[Static API Parameters]##########################
    # TC (Title Code)   { Coordinate , Bitcoin , Alarm ... (API 목적) } #
    # SC (Sub Code)            { req : request (요청) |>                #
    #                            res : resonse (응답) |>                #
    #                            fix : DB 변경 (미정) }                 #
    # returned    : API 쿼리 결과 리턴 여부                             #
    ####################################################################
    
    ##################[Weather API Key & URL]##########################################
    Weather_api_key = "---"                                                               #
    Weather_url = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst" #
    ###################################################################################
    
    Title_Code = {'Coordinate':Coordinate}
    # Sub_Code 는 Title_Code 클래스마다 별도로 지정
    
    start_server = websockets.serve(process,'192.168.56.22',8080);

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


    # 추가해야할것     # TC 에 따라 key값 선택
    # 수정해야할것     #  await 최적화 , 효율적인 변수 사용
    # 웹 서버로 재구성 필요 (웹 소켓은 1:1 연결에 좋은것 같음)


# '0.0.0.0' => 서버 pc에 ip 주소를 입력
# 0000 => 서버 pc 에 포트입력