# Generated by Django 3.0.8 on 2020-08-05 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0057_page_locale_fields_notnull'),
        ('wagtail_localize', '0004_one_source_per_objectlocale'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='translation',
            unique_together={('source', 'target_locale')},
        ),
        migrations.RemoveField(
            model_name='translation',
            name='object',
        ),
    ]
