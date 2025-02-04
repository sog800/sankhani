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

from django.contrib.auth import get_user_model
# Using get_user_model() to handle custom user models
User = get_user_model()

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delete Account Feedback from {self.user.username} on {self.created_at}"


# subscribcription

from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta

class Subscriber(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Store the form data from the frontend:
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Initially, subscribers are pending until confirmed by an admin.
    is_confirmed = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def has_expired(self):
        """Return True if the subscription is older than 32 days."""
        return timezone.now() > self.created_at + timedelta(days=32)

    def __str__(self):
        status = "Confirmed" if self.is_confirmed else "Pending"
        return f"{self.user.email} - {status}"
