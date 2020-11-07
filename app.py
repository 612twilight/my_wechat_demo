# -*- coding: utf-8 -*-
import os

from flask import Flask, request, abort, render_template
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)

# set token or get from environments
TOKEN = os.getenv("WECHAT_TOKEN", "twilight")
AES_KEY = os.getenv("WECHAT_AES_KEY", "QZZa6VCqhtZw4uLFbwXLi895zg9yGCpkz94XWNMGVDL")
APPID = os.getenv("WECHAT_APPID", "wx5c29221111cddd07")

app = Flask(__name__)
from tuning import tuning_reply
from nlpfactory import task_controller, introduction


# QZZa6VCqhtZw4uLFbwXLi895zg9yGCpkz94XWNMGVDL
#
# @app.route("/")
# def index():
#     host = request.url_root
#     return render_template("index.html", host=host)


@app.route("/", methods=["GET", "POST"])
def wechat():
    print(request.args)
    signature = request.args.get("signature", "")
    timestamp = request.args.get("timestamp", "")
    nonce = request.args.get("nonce", "")
    encrypt_type = request.args.get("encrypt_type", "raw")
    msg_signature = request.args.get("msg_signature", "")
    is_test = request.args.get("test", False)
    try:
        if not is_test:
            check_signature(TOKEN, signature, timestamp, nonce)
        pass
    except InvalidSignatureException:
        abort(403)
    if request.method == "GET":
        print("got a get request")
        echo_str = request.args.get("echostr", "")
        return echo_str

    # POST request
    if encrypt_type == "raw":
        # plaintext mode
        msg = parse_message(request.data)
        if msg.type == "text":
            # if "你是谁" in msg.content:
            #     reply = create_reply("我是月光如水的夏夜，融化冰雪的深情", msg)
            # elif "我是鸣夏" in msg.content:
            #     reply = create_reply("说啥都是爱你", msg)
            # else:
            #     relpy_text = tuning_reply(msg.content)
            relpy_text = task_controller(msg.content)
            reply = create_reply(relpy_text, msg)
        else:
            reply = create_reply("Sorry, can not handle this for now", msg)
        return reply.render()
    else:
        # encryption mode
        from wechatpy.crypto import WeChatCrypto

        crypto = WeChatCrypto(TOKEN, AES_KEY, APPID)
        try:
            msg = crypto.decrypt_message(request.data, msg_signature, timestamp, nonce)
        except (InvalidSignatureException, InvalidAppIdException):
            abort(403)
        else:
            msg = parse_message(msg)
            if msg.type == "text":
                reply = create_reply(msg.content, msg)
            else:
                reply = create_reply(introduction, msg)
            return crypto.encrypt_message(reply.render(), nonce, timestamp)


if __name__ == "__main__":
    import os

    if os.name == 'nt':
        app.run("127.0.0.1", 80, debug=True)
    else:
        app.run("172.17.0.10", 80, debug=True)
