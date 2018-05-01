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
    time_info = str(issue_time)
    if suffix_now in time_info:
        time = store_time
    elif suffix_minute in time_info:
        minute_str = issue_time.replace(suffix_minute, '')
        minutes = int(minute_str)
        time = store_time - datetime.timedelta(minutes=minutes)
    elif suffix_hour in time_info:
        hours_str = issue_time.replace(suffix_hour, '')
        hours = int(hours_str)
        time = store_time - datetime.timedelta(hours=hours)
    else:
        # time = datetime.datetime.strptime(time_info, "%Y/%m/%d %H:%M")
        time = time_info

    return time
