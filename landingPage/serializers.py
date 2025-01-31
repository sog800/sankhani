#landing page serializer

from rest_framework import serializers
from .models import LandingPage, LandingPageLink
 
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
        ]
        read_only_fields = ['id', 'user']

class LandingPageLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPageLink
        fields = ['email', 'landing_page_id']
        read_only_fields = ['email']

