import os
from logger import logger
from slack_bolt import App
from slack_sdk.web import WebClient
from dotenv import load_dotenv
from slack_sdk.errors import SlackApiError
from datetime import datetime
load_dotenv()

#load_dotenv()
LOG = logger(__name__)

# Slack APIトークンを環境変数から取得するか、直接設定します。

slack_token = os.environ.get("SLACK_BOT_TOKEN")

# Slackクライアントを初期化します。
client = WebClient(token=slack_token)

# 検索期間の開始日と終了日を指定します。
start_date = datetime(2023, 1, 1)  # 開始日を適切な日付に変更
end_date = datetime(2023, 12, 31)  # 終了日を適切な日付に変更

# チャンネル名を指定します。
channel_name = "safe-announce"  # 対象のチャンネル名
channel_id = "C05HPB9D9LN"  # 対象のチャンネル名

message = ""

# メッセージについたリアクションを集計する関数を定義します。
def get_reaction_count(channel_name, start_date, end_date):
    try:

        # 検索期間内のメッセージを取得
        messages = client.conversations_history(
            channel=channel_id,
            oldest=int(start_date.timestamp()),
            latest=int(end_date.timestamp())
        )

        user_reaction_count = {}  # ユーザーごとのリアクション数を保持する辞書
        max_user = None
        max_reactions = 0

        for message in messages["messages"]:
            user = message.get("user")
            if user:
                # メッセージについたリアクションを取得
                reactions = message.get("reactions")
                if reactions:
                    for reaction in reactions:
                        users = reaction.get("users")
                        if users:
                            for user_id in users:
                                if user_id not in user_reaction_count:
                                    user_reaction_count[user_id] = 0
                                user_reaction_count[user_id] += 1
                                # 最も多くのリアクションを持つユーザーを更新
                                if user_reaction_count[user_id] > max_reactions:
                                    max_user = user_id
                                    max_reactions = user_reaction_count[user_id]

        if max_user:
            # 最も多くのリアクションを持つユーザーとその合計を表示
            message = f"{start_date} 〜 {end_date}の集計結果\n"
            message += f"最も多くのリアクションをしたユーザー: <@{max_user}>\n 合計リアクション数: {max_reactions} \n"
            print(f"最も多くのリアクションを持ったユーザー: {max_user}")
            print(f"合計リアクション数: {max_reactions}")
        else:
            message = "指定した期間内にリアクションがついたメッセージがありませんでした。"
            print("指定した期間内にリアクションがついたメッセージがありませんでした。")
        
        if user_reaction_count:
            message += "----------------------------------------\n"
            message += "リアクションをしたユーザーと合計リアクション数:"
            print("リアクションをしたユーザーと合計リアクション数:")
            for user_id, reaction_count in user_reaction_count.items():
                user_info = client.users_info(user=user_id)
                user_name = user_info["user"]["real_name"]
                message += f"\n<@{user_id}>: {reaction_count}"
                print(f"{user_name}: {reaction_count}")
        else:
            message = "指定した期間内にリアクションがついたメッセージがありませんでした。"
            print("指定した期間内にリアクションがついたメッセージがありませんでした。")

        return message
    
    except SlackApiError as e:
        print(f"Error fetching messages: {e.response['error']}")

def send_slack_message(message):
    try:
        result = client.chat_postMessage(
            channel=channel_id,
            text=message
        )
        return result["ts"]

    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")

# リアクション数を集計
message = get_reaction_count(channel_id, start_date, end_date)
print(f"message: {message}")
message_ts = send_slack_message(message)
print(f"Message sent to Slack with timestamp: {message_ts}")