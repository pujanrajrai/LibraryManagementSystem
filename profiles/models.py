from accounts.models import MyUser
from django.db import models


# Create your models here.

class Profiles(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Rather Not Say'),
    )

    user = models.OneToOneField(MyUser, on_delete=models.PROTECT)
    profile_image = models.ImageField(blank=True, null=True)
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10, unique=True)
    dob = models.DateField(verbose_name='Date Of Birth')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    rf_id = models.CharField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return self.full_name
