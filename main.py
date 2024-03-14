# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
import os
import sys
import json

from fastapi import Request, FastAPI, HTTPException
from fastapi.responses import FileResponse

from linebot.v3.messaging import (
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

from handle_oa import OaHandler

app = FastAPI()
oa_handle = OaHandler()

domain_name = os.getenv('DOMAIN_NAME', None)

if domain_name is None:
    print('Specify DOMAIN_NAME as environment variable.')
    sys.exit(1)

@app.post("/callback/{uuid}")
async def handle_callback(uuid: str,request: Request):
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = await request.body()
    body = body.decode()
    
    # print('body',body)
    # content = json.loads(body)
    # print('destination',content['destination'])
    # parser_dict = oa_handle.get_parser_by_key(content['destination'])

    parser_dict = oa_handle.get_parser_by_key(uuid)

    parser = parser_dict['parser']
    line_bot_api = parser_dict['line_bot_api']
    line_bot_api_blob = parser_dict['line_bot_api_blob']
    base_id = parser_dict['base_id']

    try:
        events = parser.parse(body, signature)
        print(events)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        if not isinstance(event, MessageEvent):
            print("Not a MessageEvent")
            continue

        # Handling TextMessageContent (existing code remains the same)
        if isinstance(event.message, TextMessageContent):
            if event.message.text == "สวัสดี":
                message = "สวัสดีครับ"
            elif event.message.text == "base_id":
                message = f'มาจาก base_id ที่ {base_id} ครับ'
            else:
                message = event.message.text

            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=message)]
                )
            )
        # Handling ImageMessageContent (new addition)
        elif isinstance(event.message, ImageMessageContent):
            # Here you can add code to download the image or perform other actions
            # For now, let's just reply with a simple text message acknowledging the image
            future  = line_bot_api_blob.get_message_content(message_id=event.message.id, async_req=True)
            # await download_line_message_content(event.message.id)
            content = await future.get()
            if content:
                save_image_content(content, event.message.id)
                message = "Thank you for sending an image!"

                # Assume save_image_content returns the URL of the saved image
                image_url = f"{domain_name}/images/{event.message.id}"
                print(image_url)
                
                # Prepare an ImageSendMessage object with the image URL
                image_message = ImageMessage(
                    original_content_url=image_url,
                    preview_image_url=image_url  # Assuming the same URL for simplicity
                )
                
                # Reply with the image message
                await line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[image_message]
                    )
                )
            else:
                message = "Failed to download image content."
            
                await line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=message)]
                    )
                )
            
        
        else:
            message = 'เราไม่สามารถรับ format นี้ได้ครับ'
            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=message)]
                )
            )

def save_image_content(content: bytearray, message_id: str):
    # Logic to save the content to a file
    file_path = f'images/image_{message_id}.png'
    with open(file_path, 'wb') as file:
        file.write(content)
    print(f"Saved image content to {file_path}")

@app.get("/images/{image_id}")
async def serve_image(image_id: str):
    file_path = f"images/image_{image_id}.png"  # Assuming you're saving files with this naming convention
    try:
        return FileResponse(path=file_path, media_type='image/png')
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Image not found")