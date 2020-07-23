
# Fly-blog

基于Flask + Vue 构建的博客应用

网站 [光阴逆旅](https://flask.gynl.xyz/)

# 博客图片

![1](https://raw.githubusercontent.com/779505388/Fly-blog/master/example/QQ20200614-230114.png)

![2](https://raw.githubusercontent.com/779505388/Fly-blog/master/example/QQ20200614-230138.png)

# 使用方法

## 安装相关包

` pip3 install -r requirements.txt `

## 配置config 文件夹

修改 config.py ,config.json

## 配置数据库 （Mysql）

``` python

python3 manage.py init
python3 manage.py migrate
python3 manage.py upgrade

```

## 运行

` python3 service.py `

## 注册账户

 发送 json `ip:8080/api/v1/register/`

``` javascript

{"token":"123456789","register":{"mail":"","username":"","password":""}}

```

# 已完成功能

1. 文章发布、修改、删除

2. 评论发布、删除

3. 回复验证码

4. 归档

5. 文章搜索

6. 日志查看

# 待完成功能

 关于页面设置
