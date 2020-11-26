from web.hook import app, mirai
from config.config import config
import asyncio


async def authorization():
    '''启动认证'''
    await mirai.authenticate()
    await mirai.activeSession()

# 执行认证函数
asyncio.get_event_loop().run_until_complete(authorization())

# 开始运行
app.run(host='127.0.0.1', port=config['port'])
