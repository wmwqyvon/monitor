from web3 import HTTPProvider
import threading
import globalvar
from time import sleep


def watch():
    while True:
        print('running')
        sleep(1)
        if not globalvar.get_global('watcher_running'):
            print('shit!')
            break


def register(task_id: str, w3: HTTPProvider, target_type: str,
             target_address: str, interval: int) -> [threading.Thread, None]:
    for t in threading.enumerate():
        if task_id == t.name:
            return

    return threading.Thread(target=watch, name=task_id)
