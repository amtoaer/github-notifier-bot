from web.hook import app
from config.config import config
from gevent import pywsgi

# 开始运行
server = pywsgi.WSGIServer(('127.0.0.1', config['port']), app)
server.serve_forever()
