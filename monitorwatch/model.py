from peewee import *
from playhouse.mysql_ext import MariaDBConnectorDatabase, JSONField

database = MariaDBConnectorDatabase('monitorbot', user='tgbot', password='1')


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Dex(BaseModel):
    chain = CharField(null=True)
    dex_id = CharField(primary_key=True)
    factory_address = CharField(null=True)
    router_address = CharField(null=True)

    class Meta:
        table_name = 'dex'


class Token(BaseModel):
    address = CharField(primary_key=True)
    chain = CharField(null=True)
    decimals = IntegerField(null=True)
    symbol = CharField(null=True)

    class Meta:
        table_name = 'token'


class TokenPair(BaseModel):
    address = CharField(primary_key=True)
    dex_id = CharField(null=True)
    token0_address = CharField(null=True)
    token0_decimals = IntegerField(null=True)
    token0_symbol = CharField(null=True)
    token1_address = CharField(null=True)
    token1_decimals = IntegerField(null=True)
    token1_symbol = CharField(null=True)

    class Meta:
        table_name = 'token_pair'


class WatcherTask(BaseModel):
    chain = CharField(null=True)
    content = JSONField(null=True)
    interval = IntegerField(null=True)
    target_address = CharField(null=True)
    target_type = CharField(null=True)
    task_id = CharField(primary_key=True)

    class Meta:
        table_name = 'watcher_task'


class WatcherTokenRecord(BaseModel):
    record_id = CharField(primary_key=True)
    token_address = CharField(null=True)
    token_symbol = CharField(null=True)
    unit = CharField(null=True)
    buy_price = DoubleField(null=True)
    sell_price = DoubleField(null=True)
    total_supply = DoubleField(null=True)
    record_time = TimestampField(null=True)

    class Meta:
        table_name = 'watcher_token_record'
