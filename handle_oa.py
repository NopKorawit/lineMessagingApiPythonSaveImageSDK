
import os
import sys
import json
from dotenv import load_dotenv
load_dotenv()

from linebot.v3.webhook import WebhookParser
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    AsyncMessagingApiBlob,
    Configuration,
)
from line_repository import TabLineRepository
from secret import SecretUtils



class OaHandler:
    def __init__(self,select_source='db'):
        self.repository = TabLineRepository()
        self.parser_dict = {}
        self.__init_parser_dict(select_source)

    def __init_parser_dict(self,select_source):
        if select_source == 'db':
            key_str = os.getenv('SECRET_KEY_STR', None)
            if key_str is None:
                print('Specify SECRET_KEY_STR as environment variable.')
                sys.exit(1)
            self.secret = SecretUtils(key_str)
            self.__create_parser_dict_by_db()
        else:
            self.__create_parser_dict_by_env()

    def __create_parser_dict_by_db(self):
        #get mock list
        secret_list = self.repository.select_all_line_oa()
                
        for oa in secret_list:
            print(oa)
            channel_access_token = self.secret.decrypt_with_key(oa['channel_access_token'])
            configuration = Configuration(access_token=channel_access_token)
            async_api_client = AsyncApiClient(configuration)
            line_bot_api = AsyncMessagingApi(async_api_client)
            line_bot_api_blob = AsyncMessagingApiBlob(async_api_client)
            parser = WebhookParser(self.secret.decrypt_with_key(oa['channel_secret']))

            self.parser_dict[oa['uuid']] = {
                'line_bot_api':line_bot_api,
                'line_bot_api_blob':line_bot_api_blob,
                'parser':parser,
                'base_id':oa['base_id'],
            }
        print(self.parser_dict)

    def get_parser_by_key(self,key) -> dict:
        return self.parser_dict[key]
