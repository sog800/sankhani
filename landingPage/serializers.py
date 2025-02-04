#landing page serializer

from rest_framework import serializers
from .models import LandingPage, LandingPageLink, Feedback
from django.conf import settings 
 
class LandingPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPage
        fields = [
            "id",
            "title",
            "header_text",
            "header_text2",
            "business_description",
            "business_image",
            "footer_email",
            "footer_phone",
            "footer_location",
            "background_image",
            "user",
        ]
        read_only_fields = ['id', 'user']

class LandingPageLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPageLink
        fields = ['email', 'landing_page_id']
        read_only_fields = ['email']

# user feedback
# Serializer
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
        read_only_fields = ('owner', 'created_at')