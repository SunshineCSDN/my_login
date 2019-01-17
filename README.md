django注册登录
===
## 步骤
1新建项目django-admin startproject my_login
2.新建login模块  python manage.py startapp login
3.迁移数据库  python manage.py makemigratnions, python manage.py migrate
4.运行 python manage.py runserver 127.0.0.1:8000

## 开发
### 登录
1. 创建User类
2. settings installed app 插接上login模块
3. python manage.py makemigrations login , python manage.py migrate
4. python manage.py createsuperuser 
5. 访问domain:port/admin 用上一步生成的后台账户登录。
5. 往user表里添加一些测试用户
6. 设计路由
7. 开发views.py
8. session会话管理。 简单的用户名密码跟数据库信息比对成功登录后，服务器仍然还不知道这个用户登录没有，*因为http请求是无状态的*，用户再次访问某一个页面时服务器并不知道用户登录没有。解决，当用户登录成功后服务器生成sessionid自己保存一份，并在返回response时添加set-cookie(sessionid='sdkjhfakwe'),浏览器根据响应自己把sessionid保存到cookie中，之后浏览器每次请求都会携带cookie（就好像参数），服务器比对sessionid发现有就说明用户刚刚登录过，允许访问受限页面。
django_session表中存储session信息。key字段的值跟浏览器cookie中的sessionid值一致，session_data字段解密后{'is_login':True, 'username':'测试1'}
session 和cookie区分：都为了存储一些数据，都是键值对。session安全，服务器端；cookie安全低，浏览器端。
换用不同浏览器在本机模拟多用户登录。
9. 注册功能。 表单验证。前端验证体验更好，直接显示错误信息，而后端需要刷新页面才能看出。前端验证缺点被黑客直接构造请求请求后端，后端验证安全。

## 基本需求
1.简单登录
2.简单注册
3.session cookie
4.ajax表单验证
5.邮箱验证

## 追加需求
0. 修改密码功能
0. 前端美化
1. 邮件认证链接
(思路，user表新增字段active，注册保存到数据库后，取user.id,base64编码userid，拼'http://127.0.0.1:8000/active/?userid=7),往用户注册邮箱发一封邮件，邮件内容请点击激活链接，然后进入active视图函数，更新这个用户行的active字段为True。
2. 密码加密
3. （选做）OAuth
4. （选做）继承django auth模块
5. 图形验证码
6. （选做）手机接口登录（短信接口）
7. （选做）sso单点登录
8. (选做) 根据用户上次ip判断风险（github上找判断ip位置的包，通过代理进行测试）
9. 用户名限制（长度、中英文、是否重复)
10. 弱密码扫描 （github上找弱密码字典)
11. 密码强度评估（插件）
12. 滑块验证码（极验）
13. 前端数据验证
14. 同时在线人数，(查django_session表)
15. 注册表单页需要填写的内容较多，突然浏览器奔溃关闭，再次打开时自从填充已填写的内容（cookie)
16. 注册成功后帮用户自动登录（注册成功后直接写session表，响应头设置setcookie）

## 报错
1. django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module.
没有数据库驱动
解决方法一：
安装MySQLdb包，这个包底层c必须编译安装，无法直接pip安装。 https://dev.mysql.com/downloads/connector/python/ 下载对应的exe程序。mysql-connector-python.exe 。安装成功后解释器中看到mysql-connector-python 。引入import MySQLdb。
解决方法二(django官方推荐)：
MySQLdb安装麻烦，所有有人重写不依赖c编译的，但是语法和接口调用跟MySQLdb相同的包。pip install mysqlclient. 在windows上安装会直接安装.whl文件而不需要vc编译， 安装成功后会生成 xxx.pyd文件（.dll）, 安装后只能手动卸载。
解决方案三(推荐)：
pymysql以兼容MySQLdb方式启动。
根目录/my_login/__init__.py下加入下面代码
```python
import pymysql
pymysql.install_as_MySQLdb()
```
2. django.db.utils.InternalError: (1049, "Unknown database 'login'")
settings.py中配置的数据库name不存在，在数据库图形工具或终端中创建数据库create database login;
3. from django.urls import path 报错
原因安装的django为1.x老版本，语法跟2.x不同
4. unknown time zone   
原因时区名错写 Asia/Shanghai 写成大小写字母错误的其它形式。
5. 更新后的代码没效果，浏览器访问后台无日志
原因由于系统问题进程未正确结束，解决任务管理器中终止python.exe或换端口号






```

~~~
<<<from django.contrib.auth.hashers import make_password, check_password
make_password('1233456')
'pbkdf2_sha256$120000$UMroxjmVrAoa$ykEt2zxoC1uvTbVN4VC10ptY/j3sTPuIvgGwDQxuBpY='
<<<check_password('123456','pbkdf2_sha256$120000$UMroxjmVrAoa$ykEt2zxoC1uvTbVN4VC10ptY/j3sTPuIvgGwDQxuBpY=')
False
<<<check_password('1233456','pbkdf2_sha256$120000$UMroxjmVrAoa$ykEt2zxoC1uvTbVN4VC10ptY/j3sTPuIvgGwDQxuBpY=')
True

~~~