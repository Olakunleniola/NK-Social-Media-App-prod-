from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField

# Create your models here.
class Post(models.Model) : 
    text = models.CharField(max_length=240)
    date = models.DateTimeField(auto_now_add=True)
    image = ImageField(upload_to='post_images/', null=True, blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        return self.text[0:30]