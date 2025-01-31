from django.contrib import admin
from .models import CustomUser, Feedback


admin.site.register(CustomUser)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'feedback', 'created_at')
    
    # Adding 'email' to the list display by accessing the related User model's email field
    def email(self, obj):
        return obj.user.email
    email.admin_order_field = 'user__email'  # Allows sorting by email
    email.short_description = 'User Email'  # Custom column title

# Registering Feedback model with custom admin class
admin.site.register(Feedback, FeedbackAdmin)