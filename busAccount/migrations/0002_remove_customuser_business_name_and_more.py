# Generated by Django 5.1.4 on 2025-01-24 09:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('busAccount', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='business_name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='category',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='district',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_business',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='phone_number',
        ),
        migrations.CreateModel(
            name='UserBusinessProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_business', models.BooleanField(default=True)),
                ('business_name', models.CharField(blank=True, max_length=255, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('district', models.CharField(max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='businessProfile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
