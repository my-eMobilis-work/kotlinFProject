from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    def __str__(self):
        return self.username

class Appointment(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    persons = models.IntegerField()
    dateTime = models.DateTimeField()
    special_request = models.TextField()
    def __str__(self):
        return self.name


class ImageModel(models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=50)
    description = models.TextField()
    def __str__(self):
        return self.title
