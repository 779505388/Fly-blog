from functools import wraps
from flask import url_for, redirect, request,\
    session, jsonify
import hashlib
import psutil
import platform
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
