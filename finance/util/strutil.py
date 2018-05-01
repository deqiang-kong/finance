# 字符串处理
##
##
##

# 返回元组中第一个值
def getStrFirst(items):
    if len(items) > 0:
        return items[0]
    else:
        return ''


# 返回元组全部字符串
def getStrAll(items):
    if len(items) > 0:
        return ','.join(items)
    else:
        return ''
