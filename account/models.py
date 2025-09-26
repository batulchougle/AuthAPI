from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .manager import UserManager
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.

AUTH_PROVIDERS={'email':'email','google':'google'}
class User(AbstractBaseUser,PermissionsMixin):
    id = models.BigAutoField(primary_key=True, editable=False) 
    email=models.EmailField(max_length=255, unique=True, verbose_name=_("Email Address"))
    name=models.CharField(max_length=255, verbose_name=_("Name"))
    username=models.CharField(max_length=100,unique=True, verbose_name=_("Username"))
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    auth_provider=models.CharField(max_length=50,default=AUTH_PROVIDERS.get("email"))


    USERNAME_FIELD="email"

    REQUIRED_FIELDS=["name","username"]

    objects=UserManager()

    def __str__(self):
        return (self.email)
    @property
    def get_name(self):
        return (self.name)
    @property
    def get_username(self): 
        return (self.username)
    
    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return {
            'refresh':str(refresh),
            'access':str(refresh.access_token)

        }
        

class OneTimePassword(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    code=models.CharField(max_length=6, unique=True)

    def __str__(self):
        return f"{self.user.name}-passcode"