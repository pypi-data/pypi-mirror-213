# -*- coding: utf-8 -*-

'''
excel parser interfaces
'''

from datetime import datetime
from pprint import PrettyPrinter
import re
from uuid import uuid4

import pandas as pd
from peewee import (
    AutoField,
    CharField,
    DatabaseProxy,
    DateTimeField,
    fn,
    IntegerField,
    Model,
    SqliteDatabase,
)


DATABASE = DatabaseProxy()
SQLITE3_DATABASE = ''


class ExcelParse(Model):
    '''
    excel parse model
    '''

    id = AutoField()
    row = IntegerField()
    column = IntegerField()
    value = CharField()
    type = CharField()
    c_header = CharField(index=True)
    r_header = CharField(index=True)
    excel_RC = CharField(index=True)
    name = CharField(index=True)
    sheet = CharField(index=True)
    f_name = CharField(index=True)
    timestamp = DateTimeField(default=datetime.utcnow)

    @classmethod
    def get_queryset(cls, *args, **kwargs):
        '''
        return queryset with filters applied
        '''

        query = cls.filter(**kwargs)
        return pd.DataFrame(query.dicts())

    @classmethod
    def get_column(cls, column, *args, **kwargs):
        '''
        return distinct values from column with aggregations
        '''

        query = (
            cls
            .filter(**kwargs)
            .select(
                getattr(cls, column),
                fn.COUNT(cls.id).alias('Total Rows'),
                fn.COUNT(cls.type.distinct()).alias('Data Types'),
                fn.COUNT(cls.value.distinct()).alias('Distinct Values'),
            )
            .group_by(getattr(cls, column))
        )
        return pd.DataFrame(query.dicts())

    class Meta:
        database = DATABASE
        indexes = (
            (('f_name', 'sheet', 'name'), False),
        )


def parse_uri(db_str):
    '''
    parse eparse URI string
    '''

    patt = r'^(?P<endpoint>.*)://(?P<user>.*?)(:(?P<password>.*?))?(@(?P<host>.*?)(:(?P<port>.*?))?)?/(?P<name>.*)?$'  # noqa
    return re.match(patt, db_str).groupdict()


def to_null(*args, **kwargs):
    '''
    do nothing with parse data
    '''

    pass


def to_stdout(data, *args, pretty=True, **kwargs):
    '''
    print parse data to stdout
    '''

    if pretty:
        PrettyPrinter().pprint(data)
    else:
        print(data)


def to_sqlite3(data, ctx, *args, **kwargs):
    '''
    inject parse data into sqlite3 database
    '''

    global DATABASE
    global SQLITE3_DATABASE

    # this output handler requires parse -z to work
    try:
        assert ctx.obj['serialize']
    except Exception:
        raise Exception('serialize required for this interface')

    # create database if none was supplied
    if not SQLITE3_DATABASE:
        SQLITE3_DATABASE = f'.files/{uuid4()}.db'

    DATABASE.initialize(SqliteDatabase(SQLITE3_DATABASE))
    DATABASE.connect()
    DATABASE.create_tables([ExcelParse])

    # insert data into parse table
    for d in data:
        ExcelParse.create(**d)

    DATABASE.close()


def to_api(data, *args, **kwargs):
    '''
    post parse data to API endpoint
    '''

    pass


def from_sqlite3(db):
    '''
    factory to return ExcelParse model from sqlite3 db
    '''

    DATABASE.initialize(SqliteDatabase(db))
    DATABASE.connect()

    return ExcelParse
