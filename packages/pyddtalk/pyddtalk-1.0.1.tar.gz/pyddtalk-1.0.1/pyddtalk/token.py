from .base import base
from loguru import logger
import datetime


class token(base):
    def __init__(self, appKey: str, appSecret: str) -> None:
        """init

        Args:
            appKey (str): 企微appKey
            appSecret (str): 企微secret
        """
        self.appKey = appKey
        self.appSecret = appSecret
        response = self.get()
        self.token = response.get("accessToken")
        self.expires_in = response.get("expireIn")
        logger.debug(dict(msg="请求的token", token=self.token))

    def get(self):
        api_name = "oauth2/accessToken"
        params = {
            "appKey": self.appKey,
            "appSecret": self.appSecret,
        }
        response = self.request(api_name=api_name, json=params, method="POST")
        return response
