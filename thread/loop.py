import asyncio
import threading


class EventLoop(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def run(self):
        try:
            self.loop.run_forever()
        finally:
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.close()
            asyncio.set_event_loop(None)

    def run_tasks(self, coro):
        asyncio.run_coroutine_threadsafe(coro, self.loop)


event_loop = EventLoop()
event_loop.start()
