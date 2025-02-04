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

# subcription
from .models import Subscriber

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['user', 'payment_method', 'transaction_id', 'is_confirmed', 'created_at', 'updated_at']
    list_filter = ['is_confirmed', 'created_at']
    search_fields = ['user__email', 'payment_method', 'transaction_id']
    actions = ['mark_as_confirmed']

    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(is_confirmed=True)
        self.message_user(request, f"{updated} subscriber(s) marked as confirmed.")
    mark_as_confirmed.short_description = "Mark selected subscribers as confirmed"

admin.site.register(Subscriber, SubscriberAdmin)