
import os
import sys
import json
from dotenv import load_dotenv

from linebot.v3.webhook import WebhookParser
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    AsyncMessagingApiBlob,
    Configuration,
    ReplyMessageRequest,
    TextMessage,
    ImageMessage
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    ImageMessageContent
)

load_dotenv()

class OaHandler:
    def __init__(self) -> None:
        self.parser_dict = {}
        self.__create_parser_dict()

    def __create_parser_dict(self):
        #get mock list
        secret_list_str = os.getenv('SECRET_LIST_OA', None)
        print(secret_list_str)
        if secret_list_str is None:
            print('Specify SECRET_LIST as environment variable.')
            sys.exit(1)
        secret_list = json.loads(secret_list_str)
        
        for oa in secret_list:
            print(oa)
            channel_access_token = oa['channel_access_token']
            configuration = Configuration(access_token=channel_access_token)
            async_api_client = AsyncApiClient(configuration)
            line_bot_api = AsyncMessagingApi(async_api_client)
            line_bot_api_blob = AsyncMessagingApiBlob(async_api_client)
            parser = WebhookParser(oa['channel_secret'])

            self.parser_dict[oa['destination']] = {
                'line_bot_api':line_bot_api,
                'line_bot_api_blob':line_bot_api_blob,
                'parser':parser,
                'base_id':oa['base_id'],
            }

        print(self.parser_dict)
            
    def get_parser_by_destination(self,destination) -> dict:
        return self.parser_dict[destination]
