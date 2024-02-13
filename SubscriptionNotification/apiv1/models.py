from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Subscription(models.Model):
    name=models.CharField(max_length=50)
    category=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    price=models.IntegerField(default=0)

    def __str__(self):
        return self.name

class users(models.Model):
    name=models.CharField(max_length=50)
    emailid=models.CharField(max_length=255)
    phoneno=models.CharField(max_length=10)
    isSU=models.BooleanField(default=1)

    def __str__(self):
        return self.name

class SubscriptionLog(models.Model):
    user=models.ForeignKey(users, on_delete=models.CASCADE)
    subscription=models.ForeignKey(Subscription,on_delete=models.CASCADE)
    sub_type=models.CharField(max_length=255)
    ispaid=models.BooleanField(default=False)
    def __str__(self):
        return self.user.emailid+self.subscription.name+self.sub_type


class NotifierPipeline(models.Model):
    name=models.CharField(max_length=255)
    subscription=models.ForeignKey(Subscription,on_delete=models.CASCADE)
    subtype=models.CharField(max_length=255)
    subscriptionfeed=models.CharField(max_length=1000)
    issent=models.BooleanField(default=False)

    def __str__(self):
        return self.name+self.subscription.name+self.subtype+str(self.issent)





    
