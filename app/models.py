from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PassMan(models.Model):
    website = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def to_json(self):
        return {
        "website": self.website,
        "email": self.email,
        "password": self.password,
    }
    
    def __str__(self):
        return f"{self.website} with Username / Email {self.email}"