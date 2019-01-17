from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from . import models
import hashlib

# Create your views hfrom . import modelsere.
def index(request):
    return render(request, 'index.html')
    pass
def login(requset):
    if requset.method == 'GET':
        return render(requset, 'login.html')
    elif requset.method == 'POST':
        context = {
            'message':''
        }
        # 用户提交表单
        username = requset.POST.get('username')
        password = requset.POST.get('password')
        # print(username, password)
        # 查询数据库  'select * from login_user where name=%s and password=%s' % (username, password)
        # 验证账户名密码
        user = models.User.objects.filter(name=username).first()
        if user:
            if _hash_password(password) == user.hash_password:
            # if user.password == password:
                context['message'] = '登录成功'
                print(context)
                # 服务器设置sessionid和其他用户信息
                requset.session['is_login'] = True
                requset.session['username'] = user.name
                requset.session['userid'] = user.id

                return redirect('/index/')  # 返回的响应中包含set-cookie(sessionid='dkflfbf'),浏览器收到响应后会把sessionid存到cookie中。
            else:
                context['message'] = '密码不正确'
                print(context)
                return render(requset, 'login.html', context=context)
        else:
            context['message'] = '未注册'
            print(context)
            return render(requset, 'login.html', context=context)

        # if not user:
        #     # 登录失败
        #     print('用户未注册，或密码错误')
        #     return redirect('/login/')
        # else:
        #     print('注册成功')
        #     return redirect('/index/')

def register(request):
    if request.method == 'GET':
        # 注册表单
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # 简单后端表单验证(正则最适合)
        # if not(username.strip() and password.strip() and email.strip()):
        #     return render('/register', context={'message':'某个字段为空'})
        # if len(username) > 20 or len(password) > 20:
        #     print('用户名或密码长度不能超过20')
        # 排除特殊字符串 eval() \q  &$

        # 写数据库
        user = models.User.objects.filter(email=email).first()
        if user:
            return render(request, 'login.html', context={'message':'用户已注册'})
        # 'insert into login_user (name, password) values (%s, %s, %s)' % ('', '', '')

        # 加密密码
        hash_password = _hash_password(password)
        # 写数据库
        try:
            user = models.User(name=username, password=password, hash_password = hash_password, email=email)
            user.save()
            return render(request, 'login.html', context={'message':'注册成功，请继续登录'})
        except Exception as e:
            print('保存失败', e)
            return redirect('/register/')
            # return redirect(request, 'register.html', context={'message':'注册失败'})




def logout(request):
    """ 登出 """

    # 清除session 登出
    request.session.flush()  # 清除某个session键值
    # del request.session['/user_id/']  # 清除此用户sessionid对应的所有sessiondata
    return redirect('/index/')
def _hash_password(password):
    """ 哈希加密用户注册密码"""
    sha = hashlib.sha256()
    sha.update(password.encode(encoding='utf-8'))
    return sha.hexdigest()

# def _hash_password(password):
#     sha = hashlib.sha256()
#     sha.update(password.encode(encoding='utf-8'))
#     return sha.hexdigest()