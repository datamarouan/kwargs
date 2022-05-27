# Generated by Django 3.2.12 on 2022-05-27 10:57

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0004_alter_taggeditem_content_type_alter_taggeditem_tag'),
        ('projet', '0005_tache_date_butoir'),
    ]

    operations = [
        migrations.AddField(
            model_name='projet',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='Une liste de mots-clés séparés par une virgule, en minuscule', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Mots-clés'),
        ),
        migrations.AddField(
            model_name='tache',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='Une liste de mots-clés séparés par une virgule, en minuscule', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Mots-clés'),
        ),
    ]
