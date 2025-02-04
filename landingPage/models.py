#landing page model
from django.conf import settings
from django.db import models
from cloudinary.models import CloudinaryField
import cloudinary.uploader

class LandingPage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='landingPage', null=True, blank=True)
    title = models.CharField(max_length=255, default="Business Name", help_text="Title for the business.")
    header_text = models.TextField(blank=True, null=True, help_text="Text displayed in the header section.")
    header_text2 = models.TextField(blank=True, null=True, help_text="header text 2.")
    business_description = models.TextField(blank=True, null=True, help_text="Description of the business.")
    business_image = CloudinaryField('image', blank=True, null=True, help_text="Business overview image.")
    background_image = CloudinaryField('image', blank=True, null=True, help_text="header background image.")
    footer_email = models.EmailField(blank=True, null=True, help_text="Contact email for the business.")
    footer_phone = models.CharField(max_length=20, blank=True, null=True, help_text="Contact phone number.")
    footer_location = models.CharField(max_length=225, default='')

    def __str__(self):
        return self.title
    
class LandingPageLink(models.Model):
    email = models.EmailField(unique=True)  # Unique email for each user
    landing_page_id = models.IntegerField()

    def __str__(self):
        return f"Landing Page ID for {self.email}: {self.landing_page_id}"


# Model to store feedback
class Feedback(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="feedbacks")
    name = models.CharField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.owner.username} by {self.name or 'Anonymous'}"