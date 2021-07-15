# Fly-blog

基于 Flask + Vue 构建的博客应用

web: [光阴逆旅](https://flask.gynl.xyz/)

# 博客图片

![1](https://raw.githubusercontent.com/779505388/Fly-blog/master/example/20210327-213348.png)

![2](https://raw.githubusercontent.com/779505388/Fly-blog/master/example/%E6%88%AA%E5%B1%8F2021-03-27%E4%B8%8B%E5%8D%889.35.52.png)
![3](https://raw.githubusercontent.com/779505388/Fly-blog/master/example/%E6%88%AA%E5%B1%8F2021-03-27%E4%B8%8B%E5%8D%889.37.42.png)
![4](https://raw.githubusercontent.com/779505388/Fly-blog/master/example/%E6%88%AA%E5%B1%8F2021-03-27%E4%B8%8B%E5%8D%889.37.59.png)
![GITGUB提交预览](https://github.com/779505388/Fly-blog/blob/master/example/%E6%88%AA%E5%B1%8F2021-07-15%E4%B8%8A%E5%8D%8811.23.04.png?raw=true)
![登陆页面](https://github.com/779505388/Fly-blog/blob/master/example/%E6%88%AA%E5%B1%8F2021-07-15%E4%B8%8A%E5%8D%8811.24.32.png?raw=true)
![后台管理页面](https://github.com/779505388/Fly-blog/blob/master/example/%E6%88%AA%E5%B1%8F2021-07-15%E4%B8%8A%E5%8D%8811.25.30.png?raw=true)
# 使用方法

## 安装相关包

`pip3 install -r requirements.txt`

## 配置 config 文件夹

修改 config.py ,config.json

## 配置数据库 （Mysql）

```python

python3 manage.py init
python3 manage.py migrate
python3 manage.py upgrade

```

## 运行

`python3 serve.py`

## 注册账户

```javascript
//注册完成后在配置中关闭注册！！

访问 ：ip:port/register

```
