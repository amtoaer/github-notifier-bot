from web.hook import app
from config.config import config

# 开始运行
app.run(host='127.0.0.1', port=config['port'])
