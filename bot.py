import logging, os

# デバッグレベルのログを出力します
logging.basicConfig(level=logging.DEBUG)

# Web API クライアントを初期化します
from slack_sdk import WebClient
client = WebClient(os.environ["SLACK_BOT_TOKEN"])

# chat.postMessage API を呼び出します
response = client.chat_postMessage(
    channel="#random",
    text=":wave: こんにちは！",
)
