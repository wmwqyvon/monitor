from telegram.ext import Updater, Dispatcher
from signal import SIGABRT, SIGINT, SIGTERM, signal
from typing import Union, List, Tuple
from time import sleep
import importlib
import pkgutil
import logging
import globalvar
import bothandler
import watcherhandler
import web3
from model import WatcherTask
from config import BOT_TOKEN, PROVIDER

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

globalvar.init_global()
globalvar.set_global('watcher_running', True)
globalvar.set_global('logger', logging.getLogger(__name__))


def watcher_idle(stop_signals: Union[List, Tuple] = (SIGINT, SIGTERM, SIGABRT)) -> None:
    print("yep")
    def _signal_handler(signum, frame) -> None:
        print('received stop signal')
        globalvar.set_global('watcher_running', False)

    for sig in stop_signals:
        signal(sig, _signal_handler)


def start_watcher() -> None:
    tasks = WatcherTask.select()
    chains = set([t.chain for t in tasks])
    providers = {chain: web3.HTTPProvider(PROVIDER[chain]) for chain in chains}
    for task in tasks:
        if task.task_type not in [t for _, t, _ in pkgutil.iter_modules(watcherhandler.__path__)]:
            continue
        thread = importlib.import_module('watcherhandler.' + task.task_type).register(
            task.task_id, providers[task.chain], task.target_type,
            task.target_address, task.interval
        )
        if thread is not None:
            thread.start()
    watcher_idle()


def load_bot_handlers(dispatcher: Dispatcher) -> None:
    for _, module_name, _ in pkgutil.iter_modules(bothandler.__path__):
        module = importlib.import_module('bothandler.' + module_name)
        # noinspection PyUnresolvedReferences
        dispatcher.add_handler(module.handler())


def start_bot() -> None:
    updater = Updater(BOT_TOKEN)
    load_bot_handlers(updater.dispatcher)
    # updater.start_polling()
    # updater.idle()


if __name__ == '__main__':
    start_bot()
    start_watcher()
