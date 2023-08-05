from . import db
from typing import Iterable

PK, TABLE, UPDATE_BY, UPDATE_TIME, DEL_FLAG = '__pk__', '__table__', '__update_by__', '__update_time__', '__del_flag__'
SYMBOLS = ['=', '>', '<']
BETWEEN, LIKE, IN = 'between', 'like', 'in'


def _get_condition_arg(k, v):
    if not isinstance(v, str):
        return "`%s`=?" % k, v

    v_lower = v.lower()
    if any([symbol in SYMBOLS for symbol in v_lower]):
        return "`%s`%s" % (k, v), None
    elif BETWEEN in v_lower or LIKE in v_lower or IN in v_lower:
        return "`%s` %s" % (k, v), None
    else:
        return "`%s`=?" % k, v


def _get_where_arg_limit(**kwargs):
    where, args, limit = '', [], 0
    if 'limit' in kwargs:
        limit = kwargs.get('limit')
        del kwargs['limit']

    if kwargs:
        conditions, args = zip(*[_get_condition_arg(k, v) for k, v in kwargs.items()])
        args = [arg for arg in args if arg is not None]
        where = 'WHERE %s' % ' and '.join(conditions)

    return where, args, limit


def _split_ids(ids: Iterable[int], batch_size):
    ids_size = len(ids)
    mod = ids_size % batch_size
    n = ids_size // batch_size
    if mod != 0:
        n += 1

    return [ids[i:i + batch_size] for i in range(0, ids_size, batch_size)]


class Model:
    def __str__(self):
        kv = {k: v for k, v in self.__dict__.items() if not k.startswith("__")}
        return str(kv)

    def __getattr__(self, name):
        if PK == name:
            return 'id'
        elif TABLE == name:
            return self.__class__.__name__.lower()
        elif UPDATE_BY == name:
            return 'update_by'
        elif UPDATE_TIME == name:
            return 'update_time'
        else:
            return None

    def persist(self):
        kv = {k: v for k, v in self.__dict__.items() if v is not None}
        self.id = db.save(self._get_table(), **kv)
        return self.id

    def update(self):
        pk, table = self._get_pk_and_table()
        kv = {k: v for k, v in self.__dict__.items() if v is not None}
        if pk not in kv:
            raise KeyError("Not primary key.")

        update_kv = {k: v for k, v in kv.items() if k != pk}
        if update_kv:
            self.update_by_id(kv[pk], **update_kv)

    def load(self):
        pk = self._get_pk()
        kv = self.__dict__
        _id = kv.get(pk)
        if _id is not None:
            cols, _ = zip(*kv.items())
            where = 'WHERE `%s`=?' % pk
            sql = self._select_sql(where, 1, *cols)
            self.__dict__.update(db.do_select_one(sql, _id, 1))
            return self
        else:
            raise KeyError("Not primary key.")

    def delete(self):
        pk = self._get_pk()
        _id = self.__dict__.get(pk)
        if _id is None:
            raise KeyError("Not primary key.")

        return self.delete_by_id(_id)

    def logic_delete(self, update_by: int = None):
        pk = self._get_pk()
        _id = self.__dict__.get(pk)
        if _id is None:
            raise KeyError("Not primary key.")

        return self.logic_delete_by_id(_id, update_by)

    @classmethod
    def insert(cls, **kwargs):
        table = cls._get_table()
        return db.insert(table, **kwargs)

    @classmethod
    def save(cls, **kwargs):
        table = cls._get_table()
        return db.save(table, **kwargs)

    @classmethod
    def find_by_id(cls, id: int, *selection):
        """
        Return one object or None if no result.
        """
        result = cls.select_by_id(id, *selection)
        return cls._dict2obj(result) if result else None

    @classmethod
    def find_by_ids(cls, ids: Iterable[int], *selection):
        """
        Return list(object) or empty list if no result.
        """
        return [cls._dict2obj(d) for d in cls.select_by_ids(ids, *selection)]

    @classmethod
    def select_by_id(cls, id: int, *selection):
        """
        Return one row(dict) or None if no result.
        """
        pk = cls._get_pk()
        where = 'WHERE `%s`=?' % pk
        sql = cls._select_sql(where, 1, *selection)
        return db.do_select_one(sql, id, 1)

    @classmethod
    def select_by_ids(cls, ids: Iterable[int], *selection):
        """
        Return list(dict) or empty list if no result.
        """
        ids_size = len(ids)
        assert ids_size > 0, 'ids must not be empty.'

        pk = cls._get_pk()
        ids_str = ','.join(list(map(str, ids)))
        where = 'WHERE `%s` in (%s)' % (pk, ids_str)
        sql = cls._select_sql(where, ids_size, *selection)
        return db.do_select(sql, ids_size)

    @classmethod
    def update_by_id(cls, id: int, **kwargs):
        assert kwargs, 'Must set update kv'
        pk = cls._get_pk()
        where = '`%s`=?' % pk
        cols, args = zip(*kwargs.items())
        sql = cls._update_sql(where, *cols)
        return db.do_execute(sql, *args, id, 1)

    @classmethod
    def delete_by_id(cls, id: int):
        pk, table = cls._get_pk_and_table()
        sql = 'DELETE FROM `%s` WHERE `%s`=? limit ?' % (table, pk)
        return db.do_execute(sql, id, 1)

    @classmethod
    def delete_by_ids(cls, ids: Iterable[int], batch_size=128):
        ids_size = len(ids)
        assert ids_size > 0, 'ids must not be empty.'

        if ids_size == 1:
            return cls.delete_by_id(ids[0])

        if ids_size <= batch_size:
            return cls._delete_by_ids(ids)
        else:
            split_ids = _split_ids(ids, batch_size)
            with db.transaction():
                results = [cls._delete_by_ids(ids) for ids in split_ids]
            return sum(results)

    @classmethod
    def _delete_by_ids(cls, ids: Iterable[int]):
        pk, table = cls._get_pk_and_table()
        sql = 'DELETE FROM `%s` WHERE `%s` in (%s) limit ?' % (table, pk, ','.join(list(map(str, ids))))
        return db.do_execute(sql, len(ids))

    @classmethod
    def logic_delete_by_id(cls, id: int, update_by: int = None):
        pk, table = cls._get_pk_and_table()
        del_flag_col = cls._get_del_flag_col()
        update_by_col = cls._get_update_by_col()

        where = '`%s`=?' % pk
        limit = 1
        if update_by is not None and update_by_col is not None:
            sql = cls._update_sql(where, del_flag_col, update_by_col)
            return db.do_execute(sql, 1, update_by, id, limit)
        else:
            sql = cls._update_sql(where, del_flag_col)
            return db.do_execute(sql, 1, id, limit)

    @classmethod
    def logic_delete_by_ids(cls, ids: Iterable[int], update_by: int = None, batch_size=128):
        ids_size = len(ids)
        assert ids_size > 0, 'ids must not be empty.'

        if ids_size == 1:
            return cls.logic_delete_by_id(ids[0], update_by)

        if ids_size <= batch_size:
            return cls._logic_delete_by_ids(ids, update_by)
        else:
            split_ids = _split_ids(ids, batch_size)
            with db.transaction():
                results = [cls._logic_delete_by_ids(ids, update_by) for ids in split_ids]
            return sum(results)

    @classmethod
    def _logic_delete_by_ids(cls, ids: Iterable[int], update_by: int = None):
        ids_size = len(ids)
        pk = cls._get_pk()
        del_flag_col = cls._get_del_flag_col()
        update_by_col = cls._get_update_by_col()

        ids_str = ','.join(list(map(str, ids)))
        where = '`%s` in (%s)' % (pk, ids_str)
        if update_by is not None and update_by_col is not None:
            sql = cls._update_sql(where, del_flag_col, update_by_col)
            return db.do_execute(sql, 1, update_by, ids_size)
        else:
            sql = cls._update_sql(where, del_flag_col)
            return db.do_execute(sql, 1, ids_size)

    @classmethod
    def count(cls, **kwargs):
        where, args, _ = _get_where_arg_limit(**kwargs)
        selection = 'count(1)'
        limit = 1
        sql = cls._select_sql(where, limit, selection)
        return db.do_get(sql, *args, limit)

    @classmethod
    def find(cls, *selection, **kwargs):
        """
        Return list(object) or empty list if no result.
        """
        return [cls._dict2obj(d) for d in cls.select(*selection, **kwargs)]

    @classmethod
    def select(cls, *selection, **kwargs):
        """
        Return list(dict) or empty list if no result.
        """
        where, args, limit = _get_where_arg_limit(**kwargs)
        if not limit:
            limit = 1000

        sql = cls._select_sql(where, limit, *selection)
        return db.do_select(sql, *args, limit) if limit else db.do_select(sql, *args)

    @classmethod
    def _get_pk(cls):
        assert hasattr(cls, PK), "%s not set attribute '%s'" % (cls.__name__, PK)
        return cls.__pk__

    @classmethod
    def _get_table(cls):
        assert hasattr(cls, TABLE), "%s not set attribute '%s'" % (cls.__name__, TABLE)
        return cls.__table__

    @classmethod
    def _get_pk_and_table(cls):
        return cls._get_pk(), cls._get_table()

    @classmethod
    def _dict2obj(cls, dictionary):
        m = Model()
        m.__class__ = cls
        cls.__init__(m, **dictionary)
        return m

    @classmethod
    def _get_update_by_col(cls):
        if hasattr(cls, UPDATE_BY):
            return cls.__update_by__
        return None

    @classmethod
    def _get_update_time_col(cls):
        if hasattr(cls, UPDATE_TIME):
            return cls.__update_time__
        return None

    @classmethod
    def _get_del_flag_col(cls):
        assert hasattr(cls, DEL_FLAG), "%s not set attribute '%s'" % (cls.__name__, DEL_FLAG)
        return cls.__del_flag__

    @classmethod
    def _select_sql(cls, where, limit, *selection):
        table = cls._get_table()
        if len(selection) == 0:
            selection = '*'
        else:
            selection = ','.join(['%s' % col if '(' in col else '`%s`' % col for col in selection])

        if limit:
            return 'SELECT %s FROM `%s` %s limit ?' % (selection, table, where)
        else:
            return 'SELECT %s FROM `%s` %s' % (selection, table, where)

    @classmethod
    def _update_sql(cls, where, *update_cols):
        table = cls._get_table()
        update_cols = ','.join(['`%s`=?' % col for col in update_cols])
        update_time_col = cls._get_update_time_col()
        if update_time_col is not None and update_time_col not in update_cols:
            update_cols = '%s, %s' % (update_cols, '`%s`=CURRENT_TIMESTAMP' % update_time_col)

        return 'UPDATE `%s` SET %s WHERE %s limit ?' % (table, update_cols, where)

