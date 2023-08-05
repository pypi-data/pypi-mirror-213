import time
import logging
import functools
from typing import Iterable, Any
from .helper import DBCtx, ConnectionCtx, Dict, MultiColumnsError, TransactionCtx, try_commit, dynamic_sql

_DB_CTX = None
_SHOW_SQL = False
_PK_SQL = 'SELECT LAST_INSERT_ID()'


def init_db(user: str, password: str, database: str, host='127.0.0.1', port=3306, pool_size=8, use_unicode=True, show_sql=False, **kwargs):
    from mysql.connector import connect
    global _DB_CTX
    global _SHOW_SQL
    _SHOW_SQL = show_sql

    if 'mapper_path' in kwargs:
        del kwargs['mapper_path']

    if pool_size:
        kwargs['pool_size'] = pool_size
        if 'pool_name' not in kwargs:
            kwargs['pool_name'] = "%s_pool" % database

    kwargs['user'] = user
    kwargs['password'] = password
    kwargs['database'] = database
    kwargs['host'] = host
    kwargs['port'] = port
    kwargs['use_unicode'] = use_unicode
    _DB_CTX = DBCtx(lambda: connect(**kwargs))
    logging.info('Init db engine <%s> ok.' % hex(id(_DB_CTX)))


def connection():
    """
    Return _ConnectionCtx object that can be used by 'with' statement:
    with connection():
        pass
    """
    global _DB_CTX
    return ConnectionCtx(_DB_CTX)


def with_connection(func):
    """
    Decorator for reuse connection.
    @with_connection
    def foo(*args, **kw):
        f1()
        f2()
    """

    global _DB_CTX

    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with ConnectionCtx(_DB_CTX):
            return func(*args, **kw)

    return _wrapper


def transaction():
    """
    Create a transaction object so can use with statement:
    with transaction():
        pass
    >>> def update_profile(id, name, rollback):
    ...     u = dict(id=id, name=name, email='%s@test.org' % name, passwd=name, last_modified=time.time())
    ...     insert('user', **u)
    ...     r = update('update user set passwd=? where id=?', name.upper(), id)
    ...     if rollback:
    ...         raise StandardError('will cause rollback...')
    >>> with transaction():
    ...     update_profile(900301, 'Python', False)
    >>> select_one('select * from user where id=?', 900301).name
    u'Python'
    >>> with transaction():
    ...     update_profile(900302, 'Ruby', True)
    Traceback (most recent call last):
      ...
    StandardError: will cause rollback...
    >>> select('select * from user where id=?', 900302)
    []
    """
    global _DB_CTX
    return TransactionCtx(_DB_CTX)


def with_transaction(func):
    """
    A decorator that makes function around transaction.
    >>> @with_transaction
    ... def update_profile(id, name, rollback):
    ...     u = dict(id=id, name=name, email='%s@test.org' % name, passwd=name, last_modified=time.time())
    ...     insert('user', **u)
    ...     r = update('update user set passwd=? where id=?', name.upper(), id)
    ...     if rollback:
    ...         raise StandardError('will cause rollback...')
    >>> update_profile(8080, 'Julia', False)
    >>> select_one('select * from user where id=?', 8080).passwd
    u'JULIA'
    >>> update_profile(9090, 'Robert', True)
    Traceback (most recent call last):
      ...
    StandardError: will cause rollback...
    >>> select('select * from user where id=?', 9090)
    []
    """
    global _DB_CTX

    @functools.wraps(func)
    def _wrapper(*args, **kw):
        _start = time.time()
        with TransactionCtx(_DB_CTX):
            return func(*args, **kw)
        _profiling(_start)

    return _wrapper


def get(sql: str, *args, **kwargs):
    """
    Execute select SQL and expected one int and only one int result.
    MultiColumnsError: Expect only one column.
    """
    global _DB_CTX
    sql, args = dynamic_sql(sql, *args, **kwargs)
    return do_get(sql, *args)


def select_one(sql: str, *args, **kwargs):
    """
    Execute select SQL and expected one row result.
    If no result found, return None.
    If multiple results found, the first one returned.
    >>> u1 = dict(id=100, name='Alice', email='alice@test.org', passwd='ABC-12345', last_modified=time.time())
    >>> u2 = dict(id=101, name='Sarah', email='sarah@test.org', passwd='ABC-12345', last_modified=time.time())
    >>> insert('user', **u1)
    1
    >>> insert('user', **u2)
    1
    >>> u = select_one('select * from user where id=?', 100)
    >>> u.name
    u'Alice'
    >>> select_one('select * from user where email=?', 'abc@email.com')
    >>> u2 = select_one('select * from user where passwd=? order by email', 'ABC-12345')
    >>> u2.name
    u'Alice'
    """
    sql, args = dynamic_sql(sql, *args, **kwargs)
    return do_select_one(sql, *args)


def select(sql: str, *args, **kwargs):
    """
    Execute select SQL and return list or empty list if no result.
    >>> u1 = dict(id=200, name='Wall.E', email='wall.e@test.org', passwd='back-to-earth', last_modified=time.time())
    >>> u2 = dict(id=201, name='Eva', email='eva@test.org', passwd='back-to-earth', last_modified=time.time())
    >>> insert('user', **u1)
    1
    >>> insert('user', **u2)
    1
    >>> L = select('select * from user where id=?', 900900900)
    >>> L
    []
    >>> L = select('select * from user where id=?', 200)
    >>> L[0].email
    u'wall.e@test.org'
    >>> L = select('select * from user where passwd=? order by id desc', 'back-to-earth')
    >>> L[0].name
    u'Eva'
    >>> L[1].name
    u'Wall.E'
    """
    sql, args = dynamic_sql(sql, *args, **kwargs)
    return do_select(sql, *args)


def insert(table: str, **kwargs):
    """
    Execute insert SQL, return effect rowcount.
    IntegrityError: 1062 (23000): Duplicate entry '2000' for key 'PRIMARY'
    """
    sql, args = _insert_sql(table, ** kwargs)
    return do_execute(sql, *args)


def execute(sql: str, *args, **kwargs):
    """
    Execute SQL.
    """
    sql, args = dynamic_sql(sql, *args, **kwargs)
    return do_execute(sql, *args)


@with_connection
def save(table: str, **kwargs):
    """
    Execute insert SQL, return primary key.
    IntegrityError: 1062 (23000): Duplicate entry '2000' for key 'PRIMARY'
    """
    global _DB_CTX
    cursor = None
    sql, args = _insert_sql(table, ** kwargs)
    sql = _before_execute('db.save', sql, *args)
    try:
        cursor = _DB_CTX.connection.cursor()
        cursor.execute(sql, args)
        cursor.execute(_PK_SQL)
        result = cursor.fetchone()
        try_commit(_DB_CTX)
        return result[0]
    finally:
        if cursor:
            cursor.close()


@with_connection
def batch_execute(sql: str, args: Iterable[Iterable[Any]]):
    global _DB_CTX
    cursor = None
    sql = _before_execute('db.batch_execute', sql, *args)
    try:
        cursor = _DB_CTX.cursor()
        cursor.executemany(sql, args)
        effect_rowcount = cursor.rowcount
        try_commit(_DB_CTX)
        return effect_rowcount
    finally:
        if cursor:
            cursor.close()


@with_connection
def do_get(sql: str, *args):
    """
    Execute select SQL and expected one int and only one int result.
    MultiColumnsError: Expect only one column.
    """
    global _DB_CTX
    cursor = None
    if 'limit' not in sql:
        sql = '%s limit 1' % sql

    sql = _before_execute('db.do_get', sql, *args)
    try:
        cursor = _DB_CTX.cursor()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        if result:
            if len(result) == 1:
                return result[0]
            raise MultiColumnsError('Expect only one column but %d.' % len(result))
        return None
    finally:
        if cursor:
            cursor.close()


@with_connection
def do_select_one(sql: str, *args):
    """execute select SQL and return unique result or list results."""
    global _DB_CTX
    cursor = None
    if 'limit' not in sql:
        sql = '%s limit 1' % sql

    sql = _before_execute('db.do_select_one', sql, *args)
    try:
        cursor = _DB_CTX.cursor()
        cursor.execute(sql, args)
        if cursor.description:
            names = [x[0] for x in cursor.description]
            result = cursor.fetchone()
            return Dict(names, result) if result else None
        else:
            return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()


@with_connection
def do_select(sql: str, *args):
    """execute select SQL and return unique result or list results."""
    global _DB_CTX
    cursor = None
    sql = _before_execute('db.do_select', sql, *args)
    try:
        cursor = _DB_CTX.cursor()
        cursor.execute(sql, args)
        if cursor.description:
            names = [x[0] for x in cursor.description]
            return [Dict(names, x) for x in cursor.fetchall()]
        else:
            return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()


@with_connection
def do_execute(sql: str, *args):
    global _DB_CTX
    cursor = None
    sql = _before_execute('db.do_execute', sql, *args)
    try:
        cursor = _DB_CTX.connection.cursor()
        cursor.execute(sql, args)
        effect_rowcount = cursor.rowcount
        try_commit(_DB_CTX)
        return effect_rowcount
    finally:
        if cursor:
            cursor.close()


def get_connection():
    global _DB_CTX
    if _DB_CTX.is_not_init():
        _DB_CTX.init()
    return _DB_CTX.connection


def prepare(prepared=True):
    global _DB_CTX
    _DB_CTX.prepared = prepared


def _before_execute(function: str, sql: str, *args):
    global _SHOW_SQL
    if _SHOW_SQL:
        logging.info("Exec func '%s' \n\t\t  SQL: %s \n\t\t  ARGS: %s" % (function, sql, args))
    return sql.replace('?', '%s')


def _insert_sql(table: str, **kwargs):
    cols, args = zip(*kwargs.items())
    sql = 'INSERT INTO `%s` (%s) VALUES (%s)' % (table, ','.join(['`%s`' % col for col in cols]), ','.join(['?' for i in range(len(cols))]))
    return sql, args

