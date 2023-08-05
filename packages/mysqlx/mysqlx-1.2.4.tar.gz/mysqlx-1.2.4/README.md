##### Install
```
pip install mysqlx
```
##### Sample
```
from mysqlx import db

db_conf = {
    'host': HOST,
    'port': 3306, 
    'user': 'root', 
    'password': 'xxx', 
    'database': 'test',
    'pool_size': 5,
    'show_sql': True,
    # 'mapper_path': 'mapper'
}

if __name__ == '__main__':
    db.init_db(**db_conf)
    
    # Return effect rowcount
    rowcount = db.insert('user', name='张三', age=55, birth_date='1968=-10-08', sex=0, grade=1.0, point=20.5, money=854.56)
    assert rowcount == 1, 'insert'
    assert db.get('select count(1) from user') == 1, 'insert'

    # Return primery key when use auto_increment
    id2 = db.save('user', name='李四', age=55, birth_date='1968=-10-08', sex=0, grade=1.0, point=20.5, money=854.56)
    assert id2 > 0, 'save'
    # Return one value.
    assert db.get('select count(1) from user') == 2, 'save'

    db.execute('update user set name=? where id=?', '王五', id2)
    assert db.get('select name from user where id=?', id2) == '王五', 'execute'

    db.execute('update user set name=:name where id=:id', name='赵六', id=id2)
    # Return one row.
    assert db.select_one('select name from user where id=:id', id=id2)['name'] == '赵六', 'execute'

    args = [
        ('张三', 55, '1968=-10-08', 0, 1.0, 20.5, 854.56),
        ('张三', 55, '1968=-10-08', 0, 1.0, 20.5, 854.56)
    ]
    db.batch_execute('insert into user(name, age, birth_date, sex, grade, point, money) values(?,?,?,?,?,?,?)', args)
    users = db.select('select id, del_flag from user')
    assert len(users) == 4, 'batch_execute'

    users = db.select('select id, del_flag from user where id=?', id2)
    assert len(users) == 1, 'select'

    users = db.select('select id, del_flag from user where id=:id', id=id2)
    assert len(users) == 1, 'select'

    db.execute('delete from user where id=? limit 1', id2)
    assert db.get('select count(1) from user') == 3, 'execute delete'
```
##### Transaction
```
@db.with_transaction
def test_transaction():
    db.insert('user', name='张三', age=55, birth_date='1968=-10-08', sex=0, grade=1.0, point=20.5, money=854.56)
    db.insert('user', name='李四', age=55, birth_date='1968=-10-08', sex=0, grade=1.0, point=20.5, money=854.56)


def test_transaction2():
    with db.transaction():
        db.insert('user', name='张三', age=55, birth_date='1968=-10-08', sex=0, grade=1.0, point=20.5, money=854.56)
        db.insert('user', name='李四', age=55, birth_date='1968=-10-08', sex=0, grade=1.0, point=20.5, money=854.56)
```
