# Generated by Django 3.0.8 on 2020-08-21 16:52

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import uuid
import wagtail.core.blocks
import wagtail.core.fields
import wagtail_localize.test.models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0057_page_locale_fields_notnull'),
        ('wagtail_localize_test', '0002_nontranslatablesnippet'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestGenerateTranslatableFieldsPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('test_charfield', models.CharField(blank=True, max_length=255)),
                ('test_charfield_with_choices', models.CharField(blank=True, choices=[('a', 'A'), ('b', 'B')], max_length=255)),
                ('test_textfield', models.TextField(blank=True)),
                ('test_emailfield', models.EmailField(blank=True, max_length=254)),
                ('test_slugfield', models.SlugField(blank=True)),
                ('test_urlfield', models.URLField(blank=True)),
                ('test_richtextfield', wagtail.core.fields.RichTextField(blank=True)),
                ('test_streamfield', wagtail.core.fields.StreamField([('test_charblock', wagtail.core.blocks.CharBlock(max_length=255)), ('test_textblock', wagtail.core.blocks.TextBlock()), ('test_emailblock', wagtail.core.blocks.EmailBlock()), ('test_urlblock', wagtail.core.blocks.URLBlock()), ('test_richtextblock', wagtail.core.blocks.RichTextBlock()), ('test_rawhtmlblock', wagtail.core.blocks.RawHTMLBlock()), ('test_blockquoteblock', wagtail.core.blocks.BlockQuoteBlock()), ('test_structblock', wagtail.core.blocks.StructBlock([('field_a', wagtail.core.blocks.TextBlock()), ('field_b', wagtail.core.blocks.TextBlock())])), ('test_listblock', wagtail.core.blocks.ListBlock(wagtail.core.blocks.TextBlock())), ('test_nestedstreamblock', wagtail.core.blocks.StreamBlock([('block_a', wagtail.core.blocks.TextBlock()), ('block_b', wagtail.core.blocks.TextBlock())])), ('test_customstructblock', wagtail.core.blocks.StructBlock([('field_a', wagtail.core.blocks.TextBlock()), ('field_b', wagtail.core.blocks.TextBlock())]))], blank=True)),
                ('test_customfield', wagtail_localize.test.models.TestCustomField(blank=True)),
                ('test_nontranslatablesnippet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtail_localize_test.NonTranslatableSnippet')),
                ('test_snippet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtail_localize_test.TestSnippet')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='NonTranslatableChildObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('field', models.TextField()),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_nontranslatable_childobjects', to='wagtail_localize_test.TestPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TranslatableChildObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('translation_key', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('field', models.TextField()),
                ('locale', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailcore.Locale')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_translatable_childobjects', to='wagtail_localize_test.TestPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
                'unique_together': {('translation_key', 'locale')},
            },
        ),
    ]
