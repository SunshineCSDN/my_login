from django.db import models
from django.utils import timezone # timetone 时区
# Create your models here.
class User(models.Model):
    """ 用户表"""
    GENDER_CHOICE = (
        ('male', '男'),
        ('female', '女'),
        ('unknown', '未知'),
    )
    # 自增主键id,自动创建
    name = models.CharField('姓名', max_length=20)
    password = models.CharField('密码', max_length=20)
    hash_password = models.CharField('哈希密码', max_length=128, null=True, blank=True)
    gender = models.CharField('性别', choices=GENDER_CHOICE, max_length=10, default=GENDER_CHOICE[2][0])  # gender性别
    email = models.CharField('邮箱', max_length=100, unique=True)
    register_time = models.DateTimeField('注册日期', default=timezone.now)  # timezone.now不加括号
    # phone
    # last_login_time
    # is_active

    def __str__(self):
        # 默认<class User>, 重写此方法可以在调试时看到示例的name属性
        return '<class User>{}'.format(self.name)

    class Meta:
        # db_table = ''  # 默认生成 模块名_类名的表  login_user
        # ordering = ['id']  # group by
        verbose_name = '用户表'