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

    channels = ArrayField(models.ForeignKey(Channel, on_delete=models.CASCADE))
     
    tids = ArrayField(models.CharField(max_length=255,null=True, blank=True))
    def __str__(self) -> str:
        return self.name + " | " + str(self.scheduled_time) + " | " + str(self.is_running)