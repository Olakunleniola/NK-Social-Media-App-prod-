from django.db import models, IntegrityError
from django.contrib.auth.models import User

class Followers(models.Model): 
    followed_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name = "followed_by"
    )
    
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name = "following"
    )
    
    def __str__(self):
        return f"{self.followed_by.username} is following {self.following.username}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['followed_by', 'following'], name='unique_following'),
            models.CheckConstraint(check=~models.Q(followed_by=models.F('following')), name='check_following_not_same_user')
        ]