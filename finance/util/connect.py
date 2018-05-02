import pymysql
from pymysql import cursors

#
dbparams = {
    'host': 'rm-2zejbaw68504567cdgo.mysql.rds.aliyuncs.com',
    'port': 3307,
    'user': 'kongdq',
    'password': 'Qq452211',
    'database': 'test123',
    'charset': 'utf8',
    'cursorclass': cursors.DictCursor
}


# 链接数据库，判断是否存在，不存在创建
def connect_net():
    try:
        database = dbparams['database']
        dbparams.pop('database')
        # 获取一个数据库连接，注意如果是UTF-8类型的，需要制定数据库
        conn = pymysql.connect(**dbparams)
        cur = conn.cursor()
        # 确定该库是否存在
        query = "show databases like '" + database + "'"
        flag = cur.execute(query)
        if flag == 0:
            create_db(conn, database)
        else:
            conn.select_db(database)

        dbparams['database'] = database
    except Exception as e:
        print("数据库链接失败！！" + e)

    return conn


# 创建数据库
def create_db(conn, database):
    cur = conn.cursor()
    cur.execute('create database if not exists ' + database)
    conn.select_db(database)


#
# 创建数据表
def create_column_list_table(conn):
    cur = conn.cursor()  # 获取一个游标
    # 确定该表是否存在
    query = "show tables like 'column_list'"
    flag = cur.execute(query)
    if flag == 0:
        sql = '''
            create table column_list(
            id int(11) not null auto_increment primary key,
            column_id varchar(32) not null,
            title varchar(255) not null,
            img_url varchar(255) ,
            introduce varchar(255) ,
            author varchar(32) ,
            author_portrait varchar(128) ,
            pageview varchar(32) ,
            issue_time datetime ,
            store_time datetime ,
            reserved varchar(128) )DEFAULT CHARSET=utf8;
            '''
        cur.execute(sql)


# 创建数据表
def create_column_detail_table(conn):
    cur = conn.cursor()  # 获取一个游标
    # 确定该表是否存在
    query = "show tables like 'column_detail'"
    flag = cur.execute(query)
    if flag == 0:
        sql = '''
            create table column_detail(
            id int(11) not null auto_increment primary key,
            column_id varchar(32) not null,
            title varchar(255) not null,
            content longtext ,
            issue_time datetime ,
            store_time datetime ,
            reserved varchar(128) )DEFAULT CHARSET=utf8;
            '''
        cur.execute(sql)


def create_table():
    create_column_list_table(connect_net())
    create_column_detail_table(connect_net())

#
# create_table()

# dbparams = {
#            'host': '127.0.0.1',
#            'port': 3306,
#            'user': 'root',
#            'password': 'root',
#            'database': 'jianshu2',
#            'charset': 'utf8',
#            'cursorclass': cursors.DictCursor
#        }
#        # 数据库连接池
#        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
#        self._sql = None
