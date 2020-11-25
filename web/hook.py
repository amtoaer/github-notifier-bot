from graia.broadcast import Broadcast
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain
from flask import Flask
from flask import request, abort
from config.config import config
from utils.utils import Utils
import asyncio
from graia.application import GraiaMiraiApplication, Session

session_info = config['session']

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)

mirai = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host=session_info['host'],
        authKey=session_info['authKey'],
        account=session_info['account'],
        websocket=session_info['websocket'])
)

app = Flask(__name__)


@app.before_request
async def verification():
    data = request.get_data()
    try:
        if config['security']:
            if not Utils.isValid(config['token'], data,
                                 request.headers['X-Hub-Signature-256']):
                print("unpassed verification, ignored.")
                abort(400)
    except:
        print('bad request.')
        abort(400)


@app.route('/webhook', methods=['POST'])
async def handleWebhook():
    payload = request.get_data()
    try:
        targets = config["mapper"][payload["repository"]["full_name"]]
        tasks = []
        message_chain = MessageChain.create((
            Plain(Utils.generate_message(payload)),
        ))
        for group in targets['groups']:
            tasks.append(mirai.sendGroupMessage(group, message_chain))
        for friend in targets['friends']:
            tasks.append(mirai.sendFriendMessage(friend, message_chain))
        loop.run_until_complete(asyncio.wait(tasks))
    except:
        print('invalid post, ignored.\n')
