from django.contrib import admin
from .models import LandingPage, LandingPageLink, Feedback

@admin.register(LandingPage)
class LandingPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'footer_email', 'footer_phone', 'footer_location')

admin.site.register(LandingPageLink)

admin.site.register(Feedback)