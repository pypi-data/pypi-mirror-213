import os
import re
from . import db
from .helper import SqlModel
from jinja2 import Template
from typing import Iterable, Any
from .helper import DYNAMIC_REGEX, simple_sql
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

_SQL_CONTAINER = dict()


def init_db(user: str, password: str, database: str, host='127.0.0.1', port=3306, pool_size=8, use_unicode=True, show_sql=False, mapper_path='mapper',
            **kwargs):
    _load_sql(mapper_path)
    db.init_db(user, password, database, host, port, pool_size, use_unicode, show_sql, **kwargs)


def get(sql_id: str, *args, **kwargs):
    sql = get_sql(sql_id, **kwargs)
    sql, args = simple_sql(sql, *args, **kwargs)
    return db.do_get(sql, *args)


def select_one(sql_id: str, *args, **kwargs):
    sql = get_sql(sql_id, **kwargs)
    sql, args = simple_sql(sql, *args, **kwargs)
    return db.do_select_one(sql, *args)


def select(sql_id: str, *args, **kwargs):
    sql = get_sql(sql_id, **kwargs)
    sql, args = simple_sql(sql, *args, **kwargs)
    return db.do_select(sql, *args)


def insert(table: str, **kwargs):
    return db.insert(table, **kwargs)


def save(table: str, **kwargs):
    return db.save(table, **kwargs)


def execute(sql_id: str, *args, **kwargs):
    sql = get_sql(sql_id, **kwargs)
    sql, args = simple_sql(sql, *args, **kwargs)
    return db.do_execute(sql, *args)


def batch_execute(sql_id: str, args: Iterable[Iterable[Any]]):
    sql = get_sql(sql_id)
    return db.batch_execute(sql, args)


def get_connection():
    return db.get_connection()


def _get_path(path: str):
    if path.startswith("../"):
        rpath = ''.join(re.findall("../", path))
        os.chdir(rpath)
        path = path[len(rpath):]
    elif path.startswith("./"):
        path = path[2:]
    return os.path.join(os.getcwd(), path)


def _load_sql(path: str):
    if not os.path.isabs(path):
        path = _get_path(path)

    for f in os.listdir(path):
        file = os.path.join(path, f)
        if os.path.isfile(file) and f.endswith(".xml"):
            _read_mapper(file)
        elif os.path.isdir(file):
            _load_sql(file)


def _read_mapper(file: str):
    global _SQL_CONTAINER
    tree = ET.parse(file)
    root = tree.getroot()
    namespace = root.attrib.get('namespace', '')
    for child in root:
        sql_id = namespace + "." + child.attrib.get('id')
        assert sql_id not in _SQL_CONTAINER, "Sql id '%s' repeat." % sql_id
        includes = child.attrib.get('include')
        sql = child.text
        if includes or re.search(DYNAMIC_REGEX, sql):
            _SQL_CONTAINER[sql_id] = SqlModel(sql=Template(sql), dynamic=True, include=includes)
        else:
            _SQL_CONTAINER[sql_id] = SqlModel(sql=sql)


def get_sql(sql_id: str, **kwargs):
    sql_model = _get_sql_model(sql_id)
    includes = sql_model.include
    if includes:
        for include in includes.split(","):
            include_sql_id = sql_id[:sql_id.index(".")+1] + include
            kwargs[include] = get_sql(include_sql_id, **kwargs)
    return sql_model.sql.render(**kwargs) if sql_model.dynamic else sql_model.sql


def _get_sql_model(sql_id: str):
    global _SQL_CONTAINER
    return _SQL_CONTAINER[sql_id]

