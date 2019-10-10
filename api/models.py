from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)

# class UserInfo(models.Model):
#     user_type_choices = (
#         (1,'普通用户'),
#         (2,'VIP'),
#         (3,'SVIP'),
#     )
#     user_type = models.IntegerField(choices=user_type_choices)
#     username = models.CharField(max_length=32,unique=True)
#     password = models.CharField(max_length=64)

class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        self.is_actvie = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        self.is_actvie = True
        user.is_admin = True
        user.save(using=self._db)
        return user

# class UserInfo(models.Model):
#     user_type_choices = (
#         (1,'普通用户'),
#         (2,'VIP'),
#         (3,'SVIP'),
#     )
#     user_type = models.IntegerField(choices=user_type_choices)
#     username = models.CharField(max_length=32,unique=True)
#     password = models.CharField(max_length=64)

class UserInfo(AbstractBaseUser,PermissionsMixin):
    '''账号表'''
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.email

class UserToken(models.Model):
    user = models.OneToOneField(to='UserInfo',on_delete=models.CASCADE)
    token = models.CharField(max_length=64)

class Country(models.Model):
    name = models.CharField(max_length=32,verbose_name="国家")

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=32,verbose_name="城市")
    country = models.ForeignKey('Country',on_delete=models.CASCADE,verbose_name="国家")
    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(verbose_name="客户",max_length=32)
    country = models.ForeignKey('Country',on_delete=models.SET_NULL,null=True,verbose_name="国家")
    city = models.ForeignKey('City',on_delete=models.SET_NULL,null=True,verbose_name="城市")
    def __str__(self):
        return self.name


class Classes(models.Model):
    caption = models.CharField(max_length=32)

    def __str__(self):
        return self.caption

class Student(models.Model):
    name = models.CharField(max_length=32)
    cls = models.ForeignKey('Classes',on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=32)
    cls = models.ManyToManyField('Classes')

    def __str__(self):
        return self.name


class Models(models.Model):
    name = models.CharField(max_length=32)
    type = models.ForeignKey('Type',to_field='id',related_name='type_name',on_delete=models.CASCADE,verbose_name='类别')
    configure = models.OneToOneField(to='Configuration',on_delete=models.CASCADE,verbose_name='配置',null=True,blank=True)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=32,verbose_name='类别')

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=32,verbose_name='员工姓名')
    dept = models.ForeignKey('Department',on_delete=models.CASCADE,verbose_name='部门')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Configuration(models.Model):
    cpu = models.CharField(max_length=32,blank=True,null=True)
    mem = models.CharField(max_length=32,blank=True,null=True,verbose_name='内存')
    harddisk = models.CharField(max_length=32,blank=True,null=True,verbose_name='硬盘')
    gpu = models.CharField(max_length=32,blank=True,null=True,verbose_name='显卡')
    screen = models.CharField(max_length=32,blank=True,null=True,verbose_name='显示器',default='N'
                                                                                            '')

    def __str__(self):
        return 'CPU:%s 内存:%s 硬盘:%s 显卡:%s 显示器:%s' % (self.cpu,self.mem,self.harddisk,self.gpu,self.screen)

class Asset(models.Model):
    supplier_type_choices = (
        (1, 'N'),
        (2,'戴尔'),
        (3, '苹果'),
    )
    status_choices = (
        (1,'空闲'),
        (2, '使用'),
        (3, '报废')
    )
    mod = models.ForeignKey('Models',on_delete=models.CASCADE,verbose_name='型号')
    purchase_at = models.DateField(verbose_name='购买时间')
    price = models.CharField(max_length=32, verbose_name='价格',blank=True,null=True)
    recipient = models.ForeignKey('Employee',on_delete=models.CASCADE,verbose_name='领用人')
    recipient_at =  models.DateField(null=True,blank=True,verbose_name='领用时间')
    sn = models.CharField(max_length=32,verbose_name='资产编号')
    supplier = models.IntegerField(choices=supplier_type_choices,default=3,verbose_name='供应商')
    after_sales = models.CharField(max_length=128,blank=True,null=True,verbose_name='售后联系方式')
    status = models.IntegerField(choices=status_choices,default=1,verbose_name='状态')
    note = models.CharField(max_length=64,blank=True,null=True,verbose_name='备注',default='')

    def __str__(self):
        return self.sn

class Img(models.Model):
    path = models.CharField(max_length=128)

    def __str__(self):
        return self.path

class User(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = '用户表'
    def __str__(self):
        return self.name

class Role(models.Model):
    caption = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = '角色表'
    def __str__(self):
        return self.caption

class User2Role(models.Model):
    u = models.ForeignKey(User,on_delete=models.CASCADE)
    r = models.ForeignKey(Role,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = '用户分配角色'
    def __str__(self):
        return '%s-%s' % (self.u.name,self.r.caption)

class Action(models.Model):
    caption = models.CharField(max_length=64)
    code = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = '操作表'
    def __str__(self):
        return '%s' % (self.caption)

class Menu(models.Model):
    caption = models.CharField(max_length=32)
    parent = models.ForeignKey('self',related_name='p',null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.caption)

class Permission(models.Model):
    caption = models.CharField(max_length=64)
    url = models.CharField(max_length=64)
    menu = models.ForeignKey(Menu,null=True,blank=True,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'url表'
    def __str__(self):
        return '%s-%s' % (self.caption,self.url)

class Permission2Action(models.Model):
    p = models.ForeignKey(Permission,on_delete=models.CASCADE)
    a = models.ForeignKey(Action,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = '权限表'
    def __str__(self):
        return '%s-%s:%s?t=%s' % (self.p.caption,self.a.caption,self.p.url,self.a.code)

class Permission2Action2Role(models.Model):
    p2a = models.ForeignKey(Permission2Action,on_delete=models.CASCADE)
    r = models.ForeignKey(Role,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = '角色分配权限'
    def __str__(self):
        return '%s==>%s' % (self.r.caption,self.p2a)
