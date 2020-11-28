from aiohttp.client import ClientSession
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain
from flask import Flask
from flask import request, abort
from config.config import config
from utils.utils import Utils
import asyncio
from graia.application import GraiaMiraiApplication, Session
from thread.loop import event_loop

session_info = config['session']

mirai = GraiaMiraiApplication(
    broadcast=None,
    connect_info=Session(
        host=session_info['host'],
        authKey=session_info['authKey'],
        account=session_info['account'],
        websocket=session_info['websocket']),
    session=ClientSession()
)


async def authorization():
    '''启动认证'''
    await mirai.authenticate()
    await mirai.activeSession()

# 完成认证
event_loop.run_coroutine_threadsafe(authorization())


app = Flask(__name__)


@app.before_request
def verification():
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
def handleWebhook():
    payload = request.get_json()
    try:
        targets = config["mapper"][payload["repository"]["full_name"]]
        tasks = []
        message_chain = MessageChain.create((
            Plain(Utils.generate_message(payload)),
        ))
        # 将所有发送任务添加到列表
        for group in targets['groups']:
            tasks.append(mirai.sendGroupMessage(group, message_chain))
        for friend in targets['friends']:
            tasks.append(mirai.sendFriendMessage(friend, message_chain))
        # 交给事件循环执行
        event_loop.run_coroutine_threadsafe(asyncio.wait(tasks))
    except:
        print('invalid post, ignored.\n')
    finally:
        return 'ok'
