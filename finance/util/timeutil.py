# 时间处理
##
##
##

#
import datetime


# 时间换算转化
def getTimeConversion(issue_time):
    store_time = datetime.datetime.now()  # 发布时间换算
    suffix_now = '刚刚'
    suffix_minute = '分钟前'
    suffix_hour = '小时前'

    if suffix_now in issue_time:
        time = store_time
    elif suffix_minute in issue_time:
        minute_str = issue_time.replace(suffix_minute, '')
        minutes = int(minute_str)
        time = store_time - datetime.timedelta(minutes=minutes)
    elif suffix_hour in issue_time:
        hours_str = issue_time.replace(suffix_hour, '')
        hours = int(hours_str)
        time = store_time - datetime.timedelta(hours=hours)
    else:
        time = datetime.datetime.strptime(issue_time, "%Y/%m/%d %H:%M")

    return time

