from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
from landingPage.models import LandingPage
import cloudinary

class Product(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True,
    )
    landing_page = models.ForeignKey(
        LandingPage,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True
    )
    email = models.EmailField(blank=True, null=True)
    title = models.CharField(max_length=500, default="")
    product_description = models.TextField()
    product_picture = CloudinaryField("image", blank=True, null=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    professional = models.BooleanField(default=False)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)  # Field to store average rating

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Automatically link the product to the user's landing page if not already set
        if not self.landing_page and self.user:
            self.landing_page = LandingPage.objects.filter(user=self.user).first()
        super().save(*args, **kwargs)

    def update_average_rating(self):
        # Calculate the average rating for this product
        ratings = self.ratings.all()
        if ratings.exists():
            avg_rating = ratings.aggregate(models.Avg('rating'))['rating__avg']
            self.average_rating = round(avg_rating, 2)
        else:
            self.average_rating = 0.0
        self.save()

    def delete(self, *args, **kwargs):
        # Delete the image from Cloudinary when the product is deleted
        if self.product_picture:
            cloudinary.uploader.destroy(self.product_picture.public_id)
        super().delete(*args, **kwargs)


# product rating

class ProductRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 7)])  # Ratings from 1 to 6
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')  # Ensures one rating per user per product

    def __str__(self):
        return f"Rating for {self.product.title} by {self.user}"
