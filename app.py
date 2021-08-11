import random
import configparser
from flask import Flask, request, abort
from imgurpython import ImgurClient

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,
)

app = Flask(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

line_bot_api = LineBotApi('diWq0BhS0TRITsp9P7BrPxe4z90t2AKyq037qnASCYRo9jr6ACr9Im09mg3AOXDRLMdVNgrrt8lxmJGzIvEIzt6NuePuauN8aWO9ALhMD6xviEvn62j+329CDNl1YBgFgcaQtAOjXgbRUTP12gEDngdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b4f210cd6c3847435c15808ba1cb41cc')
client_id = config['imgur_api']['Client_ID']
client_secret = config['imgur_api']['Client_Secret']
album_id = config['imgur_api']['Album_ID']


@app.route("/")
def home():
    return 'home OK'

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):
    if event.message.text == "!指令":
        TextSendMessage(text=event.message.text)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='指令說明:\n'
                                                                          '\"抽\": 抽一正妹'  ))
        return 0                                              
    if event.message.text == "抽":
        TextSendMessage(text=event.message.text)
        client = ImgurClient(client_id, client_secret)
        images = client.get_album_images(album_id)
        index = random.randint(0, len(images) - 1)
        url = images[index].link
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0

if __name__ == "__main__":
    app.run()
    