from django.db import models
from django.contrib.auth.models import AbstractUser # getting the auth model to extend it
from django.db import models
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


from django.db import models
from django.conf import settings

#OneToOneField: Links each user to a single profile.
#related_name='businessProfile': Allows accessing the profile via user.businessProfile

class UserBusinessProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='businessProfile'
    )
    is_business = models.BooleanField(default=True)  # Is this a business account?
    business_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    district =  models.CharField(max_length=100, null=True) # NEED TO ADD DISTRICTS NEEDED HERE

    def __str__(self):
        return f"{self.user.username}'s Business Profile"



class Token(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    access_token = models.TextField(unique=True)
    refresh_token = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    access_expires_at = models.DateTimeField()
    refresh_expires_at = models.DateTimeField()

    def is_access_expired(self):
        return now() > self.access_expires_at

    def is_refresh_expired(self):
        return now() > self.refresh_expires_at
