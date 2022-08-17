from secrets import choice
from django.db import models
from django.contrib.auth.models import User

GENDER = (
    ('m', 'Male'),
    ('f', 'Female'),
    ('o', 'Other')
)

STATUS = (
    ('married', 'Married'),
    ('single', 'Single'),
    ('dating', 'Dating'),
    ('looking', 'Looking')
)


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.png', upload_to='profile_pics', null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length = 20, choices=GENDER, null=True, blank=True)
    status = models.CharField(max_length = 20, choices=STATUS, null=True, blank=True)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')

    def __str__(self):
        return f'{self.user.username} profile'
