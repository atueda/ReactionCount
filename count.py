import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from datetime import datetime, timedelta

# Slack APIトークン
slack_token = os.environ.get("SLACK_BOT_TOKEN")
print(os.environ)

# ワークスペース内での対象チャンネルID
channel_id = 'C05HPB9D9LN'
#token
# Slack APIクライアントの初期化
client = WebClient(token=slack_token)

# Set up the request header
headers = {
    "Authorization": f"Bearer {slack_token}",
    "Content-Type": "application/x-www-form-urlencoded"
}

def get_messages_with_reactions(start_date, end_date):
    try:
        print(f"oldest : {start_date}")
        print(f"latest : {end_date}")

        print(f"oldest : {start_date.timestamp()}")
        print(f"latest : {end_date.timestamp()}")

        result = client.conversations_history(
            channel=channel_id,
            oldest=start_date.timestamp(),
            latest=end_date.timestamp(),
        )
        print(f"result : [{result}]")
        messages = result["messages"]

        # メッセージごとにリアクション数を計算
        message_reactions = {}
        for message in messages:
            print(f"messages : [{message}]")
            if "reactions" in message:
                message_reactions[message["user"]] = message_reactions.get(message["user"], 0) + len(message["reactions"])

        # リアクション数が最大のユーザを取得
        most_reacted_user = max(message_reactions, key=message_reactions.get)
        return most_reacted_user, message_reactions[most_reacted_user]

    except SlackApiError as e:
        print(f"Error fetching messages: {e.response['error']}")

# Slackにメッセージを送信する関数
def send_slack_message(message):
    try:
        result = client.chat_postMessage(
            channel=channel_id,
            text=message
        )
        return result["ts"]

    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")

# 一定期間内のメッセージで最もリアクションの多かったユーザを取得
# start_date = datetime.now() - timedelta(days=30)  # 例: 直近30日間
# end_date = datetime.now()
start_date_august = datetime(2023, 8, 1)
end_date_october = datetime(2023, 10, 31)
most_reacted_user, reaction_count = get_messages_with_reactions(start_date_august, end_date_october)
message = f"Most Reacted User (Last 30 days): <@{most_reacted_user}> with {reaction_count} reactions"
message_ts = send_slack_message(message)
print(f"Message sent to Slack with timestamp: {message_ts}")

# 8月1日から10月までのメッセージで最もリアクションの多かったユーザを取得
start_date_august = datetime(2023, 8, 1)
end_date_october = datetime(2023, 10, 31)
most_reacted_user_aug_oct, reaction_count_aug_oct = get_messages_with_reactions(start_date_august, end_date_october)
message_aug_oct = f"Most Reacted User (Aug 1 - Oct 31): <@{most_reacted_user_aug_oct}> with {reaction_count_aug_oct} reactions"
message_ts_aug_oct = send_slack_message(message_aug_oct)
print(f"Message sent to Slack with timestamp: {message_ts_aug_oct}")

# def start_server():
#     handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
#     handler.start()