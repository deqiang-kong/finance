import datetime

from finance.util.connect import connect_net
from finance.util.timeutil import getTimeConversion


# 数据存储：专栏详情数据



# 获取表中当天已存在记录
def get_dailys_detail(conn):
    cur = conn.cursor()
    # 获取表中当天已存在的ID
    query = "select detail_url,title from column_detail where date (store_time) = curdate()"
    flag = cur.execute(query)
    dailys_detail = []
    for daily in cur.fetchmany(flag):
        dailys_detail.append(str(daily[0]))

    return dailys_detail


# 存储专栏详情信息
def store_detail(items, conn, dailys):
    cur = conn.cursor()

    title = items["title"]
    detail_url = items["detail_url"]

    if detail_url in dailys:
        print('detail 该数据已存在： ' + title)
        return

    content = items["content"]
    source = items["source"]
    author = items["author"]
    browse = items["browse"]
    compile = items["compile"]
    issue_time = items["issue_time"]

    store_time = datetime.datetime.now()
    time = getTimeConversion(issue_time)

    sql = '''
        insert into column_detail(title,detail_url,content,author,source,browse,compile,issue_time,store_time)
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s);
       '''
    try:
        cur.execute(sql, (title, detail_url, content, author, source, browse, compile, time, store_time))
        conn.commit()
        print('detail 存储成功！' + title)
    except:
        print('detail 存储失败！' + title)

    conn.commit()
    cur.close()


