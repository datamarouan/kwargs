# Generated by Django 3.2.12 on 2022-04-02 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0004_alter_taggeditem_content_type_alter_taggeditem_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Terme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('mot', models.CharField(max_length=150, verbose_name='Terme')),
                ('desc', tinymce.models.HTMLField(verbose_name='Définition(s)')),
                ('slug', models.SlugField(editable=False, max_length=255, unique=True)),
                ('created_by', models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='glossaire_terme_created', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='glossaire_terme_modified', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='Une liste de mots-clés séparés par une virgule, en minuscule', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Mots-clés')),
            ],
            options={
                'ordering': ('mot',),
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('label', models.CharField(max_length=100)),
                ('lien', models.URLField(max_length=255)),
                ('created_by', models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='glossaire_source_created', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='glossaire_source_modified', to=settings.AUTH_USER_MODEL)),
                ('terme', models.ManyToManyField(related_name='references', to='glossaire.Terme')),
            ],
            options={
                'ordering': ('label',),
            },
        ),
    ]
