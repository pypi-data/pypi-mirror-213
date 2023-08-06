import json
from ..base import base
from loguru import logger


class Message(base):
    def __init__(self, token: str, robotCode: str):
        self.robotCode = robotCode
        super().__init__(token)

    def batchSend(
        self, robotCode: str, userIds: list, msgKey: str, msgParam: str,
    ):
        api_name = "robot/oToMessages/batchSend"
        msgParam = json.dumps(msgParam)
        data = {
            "msgParam": msgParam,
            "msgKey": msgKey,
            "robotCode": robotCode,
            "userIds": userIds,
        }
        response = self.request(api_name=api_name, method="post", json=data,)
        return response

    def send_text(
        self, userIds: list, content: str,
    ):
        msgKey = "sampleText"
        msgParam = {"content": content}
        resp = self.batchSend(self.robotCode, userIds, msgKey, msgParam)
        return resp

    def send_image(self,):
        pass
