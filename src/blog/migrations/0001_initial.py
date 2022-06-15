# Generated by Django 3.2.12 on 2022-06-14 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0004_alter_taggeditem_content_type_alter_taggeditem_tag'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('titre', models.CharField(max_length=255, unique=True)),
                ('intro', models.TextField(default='')),
                ('contenu', tinymce.models.HTMLField()),
                ('slug', models.SlugField(blank=True, editable=False, max_length=255, unique=True)),
                ('published', models.BooleanField(default=False, verbose_name='Publication immédiate ?')),
                ('image', models.ImageField(default='blog/default.jpg', upload_to='blog/')),
                ('created_by', models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blog_article_created', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog_article_modified', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='Une liste de mots-clés séparés par une virgule, en minuscule', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Mots-clés')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
