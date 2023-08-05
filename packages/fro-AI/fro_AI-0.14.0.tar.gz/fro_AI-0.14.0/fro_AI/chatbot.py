import json
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from loguru import logger

URL = 'http://api.chuangfeigu.com/froapi/bot/chat'


class ChatError(Exception):
    pass


def _extract(msg):
    try:
        data = json.loads(msg)
        data = data['data']
        answer = data['answer']
        sessionId = data['sessionId']
        res = (True, answer, sessionId)

    except:
        logger.exception("error?")
        res = (False, msg)
    return res


class ChatBot():

    def __init__(self, id, apiKey) -> None:
        """聊天机器人

        Args:
            id (str): 用户 ID
            apiKey (str): API KEY
        """
        self.custId = id
        self.apiKey = apiKey
        self.sessionId = ""

    def inference(self, say):
        """聊天机器人接口

        Args:
            say (str): 聊天内容

        Returns:
            tuple: (bool, str), 若识别成功，则第一项为 True，第二项为识别结果。
                若识别失败，则第一项为 False，第二项为错误信息。
        """
        params = {
            'custId': self.custId,
            'apiKey': self.apiKey,
            'chat': say,
            'sessionId': self.sessionId
        }

        post_data = json.dumps(params, sort_keys=False)
        req = Request(URL, post_data.encode('utf-8'))
        req.add_header('Content-Type', 'application/json')
        req.add_header('appId', 'v1')
        req.add_header('sign', 'a6e1f81461204ae8b64665fe04d4eef1')
        try:
            f = urlopen(req)
            result_str = f.read()
        except URLError as err:
            print('URLError: ' + str(err.code))
            result_str = err.read()
        result = _extract(result_str)
        if len(result) == 3:
            self.sessionId = result[2]
        return result[:2]


if __name__ == "__main__":
    CUSTID = "efPRTm6MHHOyRtMj"
    APIKEY = "FB65xcK78XMROsSerGgukmN4k10w8GuJ"

    chat = ChatBot(CUSTID, APIKEY)
    ret = chat.inference("你好")
    print(ret)
    ret = chat.inference("我是")
    print(ret)
