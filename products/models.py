from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile

class Product(models.Model):
    title = models.CharField(max_length=255)
    url = models.TextField()
    pub_date = models.DateTimeField()
    count = models.IntegerField(default=1)
    image = models.ImageField(upload_to = 'images/')
    icon = models.ImageField(upload_to = 'images/')
    body = models.TextField()
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.title)

    def pub_date_preety(self):
        return self.pub_date.strftime("%b %d %Y")

    def summary(self):
        if len(self.body)<100:
            return self.body[:100]
        else:
            return self.body[:100] + "..."

class Comment(models.Model):
    commented_user = models.OneToOneField(User,on_delete=models.CASCADE)
    body = models.TextField()
    productid = models.IntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.body[:10])
