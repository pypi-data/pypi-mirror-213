# -*- coding:UTF-8 -*-
import os
import sys

import pandas as pd
import pymongo
import requests
import math

def in_severs():
    if sys.platform.startswith('linux'):
        return True
    return False


def get_mongodb():
    return os.environ.get('MONGODB_URL')

def get_db_info(db):
    db_evn = get_mongodb()
    bank_client = pymongo.MongoClient(db_evn)
    bank_col = bank_client['db-info']['raw_db']
    db_info = bank_col.find_one({'_id': db})
    if not db_info:
        db_info = bank_col.find_one({'_id': '_key_'})
        db_info['db'] = db
        del db_info['_id']
    return db_info


def df_creator(data, index=None, delitem=None):
    if delitem is None:
        delitem = []
    if index:
        df = pd.DataFrame(data, index=index)
    else:
        df = pd.DataFrame(data)
    for i in delitem:
        del df[i]
    return df


class DBWorker(object):
    def __init__(self, db):

        db_info = get_db_info(db)
        public_uri = os.environ.get('MONGODB_PUB_URI')
        uri = db_info['uri'] if in_severs() else db_info['uri'].split('@')[0] + '@' + public_uri +':'+ db_info['uri'].split(':')[
            -1]
        self.db_code = db
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[db_info['db']]
        self.col = {}

    def __link(self, col):
        if col not in self.col:
            self.col[col] = self.db[col]

    def link(self, col):
        self.__link(col)
        return self.col[col]

    def get_col_statas(self, col):
        self.__link(col)
        return self.db.command('collstats', col)

    def get_db_stats(self):
        return self.db.command('dbstats')

    def get_cols_name(self):
        return self.db.list_collection_names()

    def to_df(self, col: object, match: object = None, projection: object = None, sort: object = None, skip: object = 0,
              limit: object = 0) -> object:
        self.__link(col)
        return df_creator(
            list(self.col[col].find(filter=match, projection=projection, sort=sort, skip=skip, limit=limit)))


    def to_df_large(self, col: object, match: object = None, projection: object = None, verbose = True) -> object:
        self.__link(col)

        col_status = self.get_col_statas( col )
        st_size = col_status['size'] / 1024 / 1024
        st_count = col_status['count']
        n = math.ceil( st_size / 200 )
        step = math.ceil( st_count / n )
        if n > 1:
            if verbose:
                print( '{col} has {count:,d} records, {size:,.2f} MB, split to {n} parts'.format( col=col, count=st_count,
                                                                                      size=st_size, n=n ) )
            dfs = []
            for i in range( n ):
                if verbose:
                    print( 'processing {i:>2d} part ...'.format( i=i+1 ))
                _df = self.to_df( col, match = match, projection= projection, skip=i * step, limit=step )
                dfs.append( _df )
            df = pd.concat( dfs )
            df.drop_duplicates( subset=['_id'], inplace=True )
            df.reset_index( inplace=True, drop=True )
            if verbose:
                print( 'done' )

        else:
            df = self.to_df( col, match = match, projection= projection )

        return df

    def to_df_many(self, cols, match=None, projection=None):
        dfs = list()
        for c in cols:
            dfs.append(self.to_df_large(c, match = match, projection= projection))
        df = pd.concat(dfs)
        df.reset_index(inplace=True, drop=True)
        return df


    def insert_df(self, df, col):
        self.__link(col)
        data = df.to_dict('records')
        # data = json.loads(df.T.to_json()).values()
        self.col[col].insert_many(data)

    def update_df(self, df, col, key):
        self.__link(col)
        data = df.to_dict('records')
        # data = json.loads(df.T.to_json()).values()
        for r in data:
            self.col[col].update_one({key: r[key]}, {'$set': r}, upsert=True)

    def collection_sample(self, col, sample_size=100):
        self.__link(col)
        return self.to_df(col, limit=sample_size)

    def data_insert(self, col, data):
        self.__link(col)
        self.col[col].insert(data)

    def data_update(self, col, data):
        self.__link(col)
        self.col[col].update(data)

    def drop_col(self, col):
        self.__link(col)
        self.col[col].dorp()


def __dbmlink():
    DB_EVN = get_mongodb()
    bank_client = pymongo.MongoClient(DB_EVN)
    bank_col = bank_client['db-info']['raw_db']
    return bank_col


def dblink(db, col):
    db_info = __dbmlink().find_one({'_id': db})
    client = pymongo.MongoClient(db_info['uri'])
    db = client[db_info['db']]
    collection = db[col]
    return collection


def col_stats(db, col):
    db_info = __dbmlink().find_one({'_id': db})
    client = pymongo.MongoClient(db_info['uri'])
    db = client[db_info['db']]
    return db.command('collstats', col)


def db_stats(db):
    db_info = __dbmlink().find_one({'_id': db})
    client = pymongo.MongoClient(db_info['uri'])
    db = client[db_info['db']]
    return db.command('dbstats')


def dblink_help(db=False):
    if db:
        db_info = __dbmlink().find_one({'_id': db})
        client = pymongo.MongoClient(db_info['uri'])
        db = client[db_info['db']]
        return db.collection_names()
    else:
        dbs = __dbmlink().find()
        return [i['_id'] for i in dbs]


def df2mongo(df, col):
    data = df.to_dict('records')
    col.insert_many(data)


def mongo2df(col, match=None, projection=None, sort=None, skip=0, limit=0):
    return df_creator(list(col.find(filter=match, projection=projection, sort=sort, skip=skip, limit=limit)))


def collection_show(db, col):
    return mongo2df(dblink(db, col), limit=100)


def dblink_add(_id, uri, db=False):
    __dbmlink().insert({'_id': _id, 'uri': uri, 'db': db if db is not False else uri.split('/')[-1]})
    return _id in dblink_help()


def dblink_remove(_id):
    __dbmlink().remove({'_id': _id})


def dblink_update(_id, uri, db=False):
    __dbmlink().update({'_id': _id}, {'uri': uri, 'db': db if db is not False else uri.split('/')[-1]})


def get_token(job, on):
    db_evn = get_mongodb()
    bank_client = pymongo.MongoClient(db_evn)
    bank_col = bank_client['tk'][job]
    tk = bank_col.find_one({'on': on})
    return tk['token'], tk['servers']


def crawler_starter(db: str, col: str, work_on: str):
    db = get_db_info(db)['db']
    token, servers = get_token('crawler_starter', work_on.upper())
    body = {"db": db, "table": col, "token": token}
    return requests.post(url=servers, json=body)


def log_db(data, db):
    db = DBWorker(db)
    col = db.link('log')
    col.insert(data)


def read_log(db, _type):
    db = DBWorker(db)
    df = db.to_df("log", match={"type": _type})
    return df
