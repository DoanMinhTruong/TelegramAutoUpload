from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.
from post.models import Post
from channel.models import Channel
class Forward(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255 , blank = True, null = True)
    content = models.TextField(blank = True, null= True)
    scheduled_time = models.IntegerField(null =True, blank = True)
    is_running = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)

    channels = models.ManyToManyField(Channel, through='ForwardChannel')
     
    tid = models.CharField(max_length=255,null=True, blank=True)
    def __str__(self) -> str:
        return self.name + " | " + str(self.scheduled_time) + " | " + str(self.is_running)
    


class ForwardChannel(models.Model):
    forward = models.ForeignKey(Forward, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)


class FImage(models.Model):
    forward = models.ForeignKey(Forward, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="fimage/")
    