from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import Settings

class User(AbstractUser):
    username=None
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=12)
    is_email_verified=models.BooleanField(default=False)
    is_phone_verified=models.BooleanField(default=False)
    otp=models.CharField(max_length=6,null=True,blank=True)
    email_verification_token=models.CharField(max_length=200,null=True,blank=True)
    forget_password_token=models.CharField(max_length=200,null=True,blank=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

    objects=UserManager()

    def name(self):
        return self.first_name + ' ' +self.last_name
    
    def __str__(self):
        return self.email

# Create your models here.
@receiver(post_save,sender=User)
def send_email_token(sender,instance,created,**kwargs):
    
    try:
        subject="Your email needs to be verified"
        message=f'Hi,click on the link to verify email{uuid.uuid4()}'
        email_from=settings.EMAIL_HOST_USER
        recipent_list=[instance.email]
        send_mail(subject,message,email_from,recipent_list)
        send_mail()
    except Exception as e:
        print(e)