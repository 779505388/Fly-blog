from functools import wraps
from flask import url_for, redirect, request,\
    session, jsonify, current_app
import hashlib
import psutil
import platform
from models.Content import Category, Article
from models.Commet import Comment
import calendar
# import sys
# import os

# Md5哈希生成


def Md5(email):
    md = hashlib.md5()  # 构造一个md5
    md.update(email.encode())
    return md.hexdigest()
# 登陆限制装饰器


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not session.get('username'):
            return redirect(url_for('article.login'))
        return func(*args, **kwargs)

    return decorated_function


def get_server_info():
    test = psutil.cpu_percent(interval=None, percpu=True)
    test2 = psutil.cpu_percent(interval=None, percpu=False)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    swap = psutil.swap_memory()
    cpu_freq = psutil.cpu_freq()
    data = {
        'cpu_test': round(test2/100, 3),
        'cpu_percent': test2,
        'cpu_count': psutil.cpu_count(),
        'memory_percent': round((memory.used/memory.total)*100, 3),
        'memory_total': round(memory.total/1024**3, 2),
        'memory_used': round(memory.used/1024**3, 2),
        'disk_total': round(disk.total/1024**3, 2),
        'disk_used': round(disk.used/1024**3, 2),
        'disk_percent': ((disk.used/disk.total)*100),
        'swap_percent': (swap.used/2)*100,
        'swap_total': round(swap.total/1024**3, 2),
        'swap_used': round(swap.used/1024**3, 2)
    }
    return data


def sys_name():
    # 判断系统类型
    return platform.system()


def get_month_range(start_day, end_day):
    # 处理日期
    months = (end_day.year - start_day.year) * \
        12 + end_day.month - start_day.month
    month_range = ['%s-%s' % (start_day.year + mon//12, mon % 12+1)
                   for mon in range(start_day.month-1, start_day.month + months)]
    return month_range


def getCategory():
    data = Category.query.all()
    names = []
    for i in data:
        names.append(i.name)
    return names


def get_month_days(time):
    """
    根据年份，月份信息显示此月份天数
    :param year: 年份：
    :param month: 月份（1～12）：
    :return: 当月天数
    """
    a = time.split('-')
    year = int(a[0])
    month = int(a[1])
    if month > 12 or month <= 0:
        return -1
    if month == 2:
        return 29 if year % 4 == 0 and year % 100 != 0 or year % 400 == 0 else 28

    if month in (4, 6, 9, 11):
        return 30
    else:
        return 31


def getItem():
    articleNum = Article.query.count()
    commentNum = Comment.query.count()
    return {"articleNum": articleNum, 'commentNum': commentNum}


def getInfo():
    return current_app.config.get("INFO")
