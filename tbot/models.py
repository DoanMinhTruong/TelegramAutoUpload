from django.db import models
# from user.models import User
# Create your models here.
class Tbot(models.Model):
    name = models.CharField(max_length=255 , unique = True, blank = False)
    # type = models.CharField(max_length=255 , blank= False)
    description = models.CharField(max_length=255)
    link = models.CharField(max_length=255 , blank = False, null =False)
    token = models.CharField(max_length=255 , blank = False, null = False) 
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.name + " | " + self.link
    class Meta:
        db_table = 'tbot'