from re import S
from flask import Flask, render_template, request
from model import WatcherTask, WatcherTokenRecord
import json

app = Flask(__name__)





@app.route("/info")
def info():
    tasks = WatcherTask.select()
    tokens = [(t.task_id, t.target_address) for t in tasks]


    return render_template('info.html', tokens=tokens)


@app.route("/info/data", methods=['GET'])
def get_data():
    token_address = request.args.get("token")
    time_span = request.args.get("time")
    x = request.args.get("x")

    try: 
        sample_n_x = int(x)
    except:
        sample_n_x = 10

    multiplier = {
        '3m': 1,
        '15m': 5,
        '1h': 20,
        '4h': 80,
        '1d': 480,
    }

    all_sample_n = multiplier.get(time_span) * sample_n_x
    if all_sample_n is None:
        return r'{"status":-1,"info":"invalid_time_span"}'
    total_records_n = WatcherTokenRecord.select(WatcherTokenRecord.token_address == token_address).count()
    if all_sample_n > total_records_n:
        return r'{"status":0,"info":"token_data_not_prepared"}'
    records = WatcherTokenRecord.select().where(WatcherTokenRecord.token_address == token_address).order_by(WatcherTokenRecord.record_time.desc()).limit(all_sample_n)
    token_info = records.get()


    return json.dumps({
        "status": 1,
        "info": "success",
        "result": {
            "token": token_address,
            "symbol": token_info.token_symbol,
            "unit": token_info.unit,
            "multi": multiplier.get(time_span),
            "time_span": time_span,
            "data": [{
                "timestamp": r.record_time,
                "buy_price": r.buy_price,
                "sell_price": r.sell_price,
                "total_supply": r.total_supply
            } for r in records]
        }
    })