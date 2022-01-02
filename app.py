import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage,AudioSendMessage,ImageSendMessage

from fsm import TocMachine
from utils import send_text_message
import message
load_dotenv()

user_id = []
#state1:選擇看影片 state2:選擇看梗圖  state3:評論 state4:讚+回家 state5:倒讚+回家
machine = TocMachine(
    states=["user", "state1", "state2","state3","state4","state5"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",                                      #0 to 1
            "dest": "state1",
            "conditions": "is_going_to_state1",
        },
        {
            "trigger": "advance",
            "source": "user",                                   # 0 to 2
            "dest": "state2",
            "conditions": "is_going_to_state2",
        },
        {
            "trigger": "advance",
            "source": "state1",                                 #1 to 2
            "dest": "state2",
            "conditions": "state1_going_to_state2",
        },
        {
            "trigger": "advance",
            "source": "state1",                                 #1 to 3
            "dest": "state3",
            "conditions": "is_going_to_state3",
        },
        {
            "trigger": "advance",
            "source": "state2",                             # 2 to 1
            "dest": "state1",
            "conditions": "state2_going_to_state1",
        },
        {
            "trigger": "advance",
            "source": "state2",                             # 2 to 2
            "dest": "state2",
            "conditions": "state2_loop",
        },
        {
            "trigger": "advance",
            "source": "state2",                             # 2 to 3
            "dest": "state3",
            "conditions": "is_going_to_state3",
        },
        {
            "trigger": "advance",
            "source": "state3",
            "dest": "state4",                               # 3 to 4
            "conditions": "is_going_to_state4",
        },
        {
            "trigger": "advance",
            "source": "state3",                             # 3 to 5
            "dest": "state5",
            "conditions": "is_going_to_state5",
        },
        {
            "trigger": "advance",
            "source": "state4",                             #4   to user                           
            "dest": "user",
            "conditions": "is_going_to_user",
        },
        {
            "trigger": "advance",
            "source": "state5",                             #5 to user
            "dest": "user",
            "conditions": "is_going_to_user",
        },
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        if event.source.user_id not in user_id:
            id = event.source.user_id
            user_id.append(id)
            message_text = message.main_menu
            reply = FlexSendMessage("主選單", message_text)
            line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
            line_bot_api.push_message(id,reply)
        else:
            response = machine.advance(event)
            if response == False:
                send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    #port = os.getenv("PORT", None)
    app.run(host="0.0.0.0", port=port, debug=True)
