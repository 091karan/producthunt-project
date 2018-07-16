from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images/',null=True)
    birth_date = models.DateTimeField(null=True,blank=True)
    bio = models.TextField(max_length=500,blank=True,default='')
    website = models.URLField(default='',max_length=100,blank=True)
    phone = models.CharField(max_length=100,blank=True,default='')
    city = models.CharField(max_length=500,blank=True,default='')
    country = models.CharField(max_length=500,blank=True,default='')

    def __str__(self):
        return '{}'.format(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
