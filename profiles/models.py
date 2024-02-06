from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# from sorl.thumbnail import ImageField
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model) : 
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        # related_name = 'profile'
    )
    image = CloudinaryField('image')
    backdrop_image = CloudinaryField('backdrop_image')
    
    def __str__(self) : 
        return f'{self.user.username} {self.user.last_name}'
    
@receiver(post_save, sender=User)
def create_user_profile (sender, instance, created, **kwargs) : 
    """Create a new Profile() object whenever a django user is created"""
    if created: 
        Profile.objects.create(user=instance)