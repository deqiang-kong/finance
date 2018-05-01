import pymysql

# 数据库连接信息
host = 'rm-2zejbaw68504567cdgo.mysql.rds.aliyuncs.com'
port = 3307
user = 'kongdq'
passwd = 'Qq452211'
db_name = 'asdf'


# 链接数据库，判断是否存在，不存在创建
def connect_net():
    try:
        # 获取一个数据库连接，注意如果是UTF-8类型的，需要制定数据库
        conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, charset='utf8')

        cur = conn.cursor()
        # 确定该表是否存在
        query = "show databases like '" + db_name + "'"
        flag = cur.execute(query)
        if flag == 0:
            create_db(conn)
        else:
            conn.select_db(db_name)

    except Exception as e:
        print("数据库链接失败！！" + e)

    return conn


# 创建数据库
def create_db(conn):
    cur = conn.cursor()
    cur.execute('create database if not exists ' + db_name)
    conn.select_db(db_name)


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
            title varchar(255) not null,
            detail_url varchar(255) not null,
            introduce varchar(255) ,
            author varchar(32) ,
            author_portrait varchar(128) ,
            browse varchar(32) ,
            label varchar(128) ,
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
            title varchar(255) not null,
            detail_url varchar(255) not null,
            content longtext ,
            author varchar(32) ,
            browse varchar(32) ,
            source varchar(128) ,
            compile varchar(128) ,
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
