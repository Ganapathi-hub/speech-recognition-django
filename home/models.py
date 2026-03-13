from django.db import models
from django.contrib.auth.models import User

class LoginAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)

    def __str__(self):
        return f"LoginAttempt(user={self.user.username}, success={self.success}, timestamp={self.timestamp})"

class Feedback(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.name



# Create your models here.
