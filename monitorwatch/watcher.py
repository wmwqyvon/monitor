from web3 import Web3
from web3.eth import Contract
import threading
import globalvar
from uuid import uuid4
from model import Token, TokenPair, WatcherTokenRecord, Dex, DoesNotExist
from time import sleep
from buffer import watcher_token_queue
from abi import *


def watcher_writer():
    while True:
        if not globalvar.get_global('watcher_running'):
            break
        if watcher_token_queue.qsize() >= 10:
            records = []
            for _ in range(watcher_token_queue.qsize()):
                records.append(watcher_token_queue.get())
            print(records)
            WatcherTokenRecord.insert_many(records).execute()


def get_token_info(token: Contract, pair: Contract, router: Contract,
                   token0_address, token1_address,
                   token0_symbol, token1_symbol,
                   token0_decimals, token1_decimals):
    total_supply = token.functions.totalSupply().call()

    token0_reserves, token1_reserves, t = pair.functions.getReserves().call()
    reserves = (token0_reserves, token1_reserves, token0_symbol, token1_symbol, token0_decimals, token1_decimals) \
        if token.address == token0_address else \
        (token1_reserves, token0_reserves, token1_symbol, token0_symbol, token1_decimals, token0_decimals)
    sell_amount = router.functions.getAmountIn(int(10 ** reserves[5]), reserves[0], reserves[1]).call()
    buy_amount = router.functions.getAmountOut(int(10 ** reserves[5]), reserves[1], reserves[0]).call()
    watcher_token_queue.put({
        'record_id': str(uuid4()),
        'token_address': token.address,
        'token_symbol': reserves[2],
        'unit': reserves[3],
        'buy_price': 10 ** reserves[4] / buy_amount,
        'sell_price': 10 ** reserves[4] / sell_amount,
        'total_supply': total_supply,
        'record_time': int(t)
    })


def watch(w3: Web3, target_type, target_address, interval, content):
    if target_type == 'token':
        try:
            # token = Token.get(Token.address == target_address)
            token_pair = TokenPair.get(TokenPair.address == content['token_pair'])
            dex = Dex.get(Dex.dex_id == token_pair.dex_id)

            token_contract = w3.eth.contract(target_address, abi=TOKEN_ABI)
            pair_contract = w3.eth.contract(content['token_pair'], abi=PAIR_ABI)
            router_contract = w3.eth.contract(dex.router_address, abi=ROUTER_ABI)

            while True:
                get_token_info(
                    token_contract, pair_contract, router_contract,
                    token_pair.token0_address, token_pair.token1_address,
                    token_pair.token0_symbol, token_pair.token1_symbol,
                    token_pair.token0_decimals, token_pair.token1_decimals,
                )
                sleep(interval)
                # break
                if not globalvar.get_global('watcher_running'):
                    break
        except DoesNotExist:
            pass


def register(task_id: str, w3: Web3, target_type: str,
             target_address: str, interval: int, content):
    for t in threading.enumerate():
        if task_id == t.name:
            return

    return threading.Thread(
        target=watch, name=task_id,
        args=(w3, target_type, target_address, interval, content,)
    )
