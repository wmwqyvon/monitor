from signal import SIGABRT, SIGINT, SIGTERM, signal
import threading
import globalvar
import watcher
import web3
from model import WatcherTask
from config import PROVIDER


globalvar.init_global()
globalvar.set_global('watcher_running', True)

def start_watcher() -> None:
    tasks = WatcherTask.select()
    chains = set([t.chain for t in tasks])
    providers = {chain: web3.Web3(web3.HTTPProvider(PROVIDER[chain])) for chain in chains}
    for task in tasks:
        thread = watcher.register(
            task.task_id, providers[task.chain], task.target_type,
            task.target_address, task.interval, task.content
        )
        if thread is not None:
            thread.start()
    threading.Thread(target=watcher.watcher_writer).start()

    def _signal_handler(signum, frame) -> None:
        globalvar.set_global('watcher_running', False)

    for sig in (SIGINT, SIGTERM, SIGABRT):
        signal(sig, _signal_handler)



if __name__ == '__main__':
    start_watcher()
