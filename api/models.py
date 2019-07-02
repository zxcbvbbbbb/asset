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

class Img(models.Model):
    path = models.CharField(max_length=128)

    def __str__(self):
        return self.path