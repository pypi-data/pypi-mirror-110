# Generated by Django 3.1.6 on 2021-02-19 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtail_localize', '0012_localesynchronization'),
    ]

    operations = [
        migrations.AddField(
            model_name='translationsource',
            name='schema_version',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
