MySQL Python Class
===========

`mysql_connect.py`对应的是[mysql.connector](https://dev.mysql.com/doc/connector-python/en/)
`mysql_python.py`对应的是MySQLdb，这个我直接从[nestordeharo](https://github.com/nestordeharo/mysql-python-class) fork过来的。

你需要import类并初始化`host`,`user`,`password`,`database`四个参数来开始使用

```python
from mysql_connect import MysqlConnect

connect_mysql = MysqlPython('host.ip.address', 'user', 'password', 'database')
```

### Select语句带一个条件

如果你查询语句只涉及一个表和一个条件，那你可以使用`select`函数，`args`参数写你要获取的列名。

```python
  conditional_query = 'car_make = %s '

  result = connect_mysql.select('car', conditional_query, 'id_car', 'car_text', car_make='nissan')
```

**返回结果:** 函数返回一个列表，若未获取到数据则返回空列表

### Select语句带多个条件(mysql_python.py)

如果你的where条件超过一个，请使用`select_advanced`函数，`args`参数会转为`tuple`。

```Python
  sql_query = 'SELECT C.cylinder FROM car C WHERE C.car_make = %s AND C.car_model = %s'

  result = connect_mysql.select_advanced(sql_query, ('car_make', 'nissan'),('car_model','altima'))
```

_注意:在`sql_advanced`函数中`tuple`要按顺序传_

**返回结果:** 函数返回一个列表，若未获取到数据则返回空列表

### 复杂Select语句(mysql_connect.py)

复杂语句就直接用这个吧。

```Python
query = ("SELECT first_name, last_name, hire_date FROM employees "
         "WHERE hire_date BETWEEN %s AND %s")

hire_start = datetime.date(1999, 1, 1)
hire_end = datetime.date(1999, 12, 31)

result = connect_mysql.select_advanced(query, (hire_start, hire_end))
```

**返回结果:** 函数返回一个列表，若未获取到数据则返回空列表

### 插入数据

插入数据非常简单，指定列名和值即可

```Python
  result = connect_msyql.insert('car', car_make='ford', car_model='escort', car_year='2005')
```

**返回结果:** 该函数返回最后一个插入数据的row id

### 批量插入(mysql_connect.py)

批量插入数据，mysql.connect会自动拼接语句

```Python
data = [
  ('Jane', date(2005, 2, 12)),
  ('Joe', date(2006, 5, 23)),
  ('John', date(2010, 10, 3)),
]
stmt = "INSERT INTO employees (first_name, hire_date) VALUES (%s, %s)"
connect_mysql.insert_bulk(stmt, data)
```

### 更新数据

要更新数据，指定表名，条件和字段就可以了。

```Python
conditional_query = 'car_make = %s'

result = connect_mysql.update('car_table', conditional_query, 'nissan', car_model='escort', car_year='2005')
```

**返回结果:** 该函数返回被修改的数量

### 复杂更新数据(mysql_connect.py)

复杂语句就直接用这个吧。

```Python
stmt = '''
    update bussiness_table
    set businesstype=20 
    where id in (''' + ','.join(id_list) + ''')
    '''

    result = connect_mysql.update_advanced(stmt)
```

**返回结果:** 该函数返回被修改的数量

### 删除数据

删除数据很简单，表名，字段名和条件即可

```Python
  conditional_query = 'car_make = %s'

  result = connect_mysql.delete('car', conditional_query, 'nissan')
```

**返回结果:** 返回删除的行数

