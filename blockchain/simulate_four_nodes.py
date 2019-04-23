from threading import Thread

from main import run

for ip in range(5000, 5005):
    t = Thread(target=run, args=("127.0.0.1", str(ip)))
    t.start()
