from rest_framework import serializers
from .models import Product, ProductRating

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "user",
            'landing_page',
            "email",
            "title",
            "product_description",
            "product_picture",
            "district",
            "professional",
            "category",
            "average_rating"
        ]
        read_only_fields = ["email", "user"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        validated_data["email"] = user.email
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