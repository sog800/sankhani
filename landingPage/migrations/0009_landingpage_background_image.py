# Generated by Django 5.1.5 on 2025-02-04 05:52

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landingPage', '0008_rename_message_feedback_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='landingpage',
            name='background_image',
            field=cloudinary.models.CloudinaryField(blank=True, help_text='header background image.', max_length=255, null=True, verbose_name='image'),
        ),
    ]
