import datetime
import time


# 获取当前时间
def date(y: int, m: int, d: int):
    return datetime.date(y, m, d)


# 获取当前年月日
def today():
    return datetime.date.today()


# 获取当前时间 YYYY-MM-DD hh-mm-ss
def now():
    date_str = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())
    return date_str


# 格式化当前时间 -- 支持使用 python 形式通配符
def parse(f="yyyy/MM/dd HH:mm:ss"):
    localTime = time.localtime()
    if f == 'yyyy/MM/dd HH:mm:ss':
        return time.strftime('%Y/%m/%d  %H:%M:%S', localTime)
    elif f == 'yyyy年MM月dd日 HH时mm分ss秒':
        return time.strftime('%Y年%m月%d日  %H时%M分%S秒', localTime)
    elif f == 'yyyy-MM-dd':
        return time.strftime('%Y-%m-%d', localTime)
    elif f == 'yyyy/MM/dd':
        return time.strftime('%Y/%m/%d', localTime)
    else:
        return time.strftime(f, localTime)


# 获取当前日期年份
def year(d: datetime.date):
    return d.today().year


#
# def year(d: date()):
#     return d.year


# 获取当前日期月份
def month(d: datetime.date):
    return d.today().month


# def month(d: date()):
#     return d.month


# 获取当前日期天
def day(d=datetime.date):
    return d.today().day


# def day(d: date()):
#     return d.day


if __name__ == '__main__':
    print(parse("%Y*%M"))
    print(day())
    print(today())
