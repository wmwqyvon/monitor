from peewee import *

database = MySQLDatabase('monitorbot', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'user': 'tgbot', 'password': '1'})

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
    token0_symbol = CharField(null=True)
    token1_address = CharField(null=True)
    token1_symbol = CharField(null=True)

    class Meta:
        table_name = 'token_pair'

class WatcherTask(BaseModel):
    chain = CharField(null=True)
    interval = IntegerField(null=True)
    target_address = CharField(null=True)
    target_type = CharField(null=True)
    task_id = CharField(primary_key=True)
    task_type = CharField(null=True)

    class Meta:
        table_name = 'watcher_task'

