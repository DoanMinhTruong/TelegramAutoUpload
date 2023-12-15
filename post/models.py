from django.db import models
from channel.models import Channel
from django.utils import timezone
from background_task import background
import telebot
from backend.background import BackgroundScheduler

def send(bot_token , channel):
    bot = telebot.TeleBot(bot_token)
    channel_link = "@" + channel_link.split('/')[-1]
    try:
        message = bot.send_message(channel_link, message)
    except:
        return


class Post(models.Model):
    channel = models.ForeignKey(Channel , on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255 , blank = True, null = True)
    content = models.TextField(blank = True, null= True)
    scheduled_time = models.IntegerField(null =True, blank = True)
    is_running = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    tid = models.CharField(max_length=255,null=True, blank=True)

        

class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image/")

