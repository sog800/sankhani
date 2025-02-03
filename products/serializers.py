from rest_framework import serializers
from .models import Product, ProductRating
from landingPage.models import LandingPage

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "user",
            "landing_page",
            "email",
            "title",
            "product_description",
            "product_picture",
            "district",
            "professional",
            "category",
            "average_rating",
        ]
        read_only_fields = ["email", "user", "landing_page"]  # User & landing_page should not be provided in request

    def create(self, validated_data):
        """Ensure user and email are set correctly when creating a product."""
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError({"error": "User authentication failed."})

        user = request.user
        landing_page = LandingPage.objects.filter(user=user).first()

        if not landing_page:
            raise serializers.ValidationError({"error": "User must have a landing page before creating a product."})

        validated_data["user"] = user
        validated_data["email"] = user.email
        validated_data["landing_page"] = landing_page

        return super().create(validated_data)


# product rating

class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = ['product', 'rating']

    def validate_rating(self, value):
        if value < 1 or value > 6:
            raise serializers.ValidationError("Rating must be between 1 and 6.")
        return value