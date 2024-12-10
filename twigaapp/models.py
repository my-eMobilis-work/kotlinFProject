from django.db import models


class Users(models.Model):
    username = models.CharField(max_length=70)
    phone = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    password = models.CharField(max_length=300)
    dateJoined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Managers(models.Model):
    manager_name = models.CharField(max_length=70)
    image = models.ImageField(upload_to='dashboard_profiles/', null=True, blank=True)
    password = models.CharField(max_length=300)
    phone = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    dateJoined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.manager_name


class Contacts(models.Model):
    name = models.CharField(max_length=70)
    phone = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    subject = models.CharField(max_length=50)
    message = models.TextField(max_length=250)

    def __str__(self):
        return self.name


class Bookings(models.Model):
    type = models.CharField(max_length=20)
    paid = models.BooleanField(default=False)
    name = models.CharField(max_length=25)
    phone = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    dateTime = models.DateTimeField()
    persons = models.IntegerField()
    specialRequest = models.TextField(null=True, blank=True)
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ImageModels(models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
