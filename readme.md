
# Fly-blog

基于Flask + Vue 构建的博客应用

web: [光阴逆旅](https://flask.gynl.xyz/)

# 博客图片

![1](https://raw.githubusercontent.com/779505388/Fly-blog/master/example/20210327-213348.png)

![2](https://raw.githubusercontent.com/779505388/Fly-blog/master/example/%E6%88%AA%E5%B1%8F2021-03-27%E4%B8%8B%E5%8D%889.35.52.png)
![3](https://raw.githubusercontent.com/779505388/Fly-blog/master/example/%E6%88%AA%E5%B1%8F2021-03-27%E4%B8%8B%E5%8D%889.37.42.png)
![4](https://raw.githubusercontent.com/779505388/Fly-blog/master/example/%E6%88%AA%E5%B1%8F2021-03-27%E4%B8%8B%E5%8D%889.37.59.png)

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

` python3 serve.py `

## 注册账户


 发送 json `ip:8080/api/v1/register/`

``` javascript
//token=>在api/v1/token.py设置

{"token":"123456789","register":{"mail":"","username":"","password":""}}

```

