# Generated by Django 3.2.12 on 2022-06-14 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import rudi.models
import simple_history.models
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0004_alter_taggeditem_content_type_alter_taggeditem_tag'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalDocument',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('identification', models.CharField(default=uuid.uuid4, editable=False, max_length=36)),
                ('fichier', models.TextField(max_length=255, verbose_name='Document')),
                ('nom', models.CharField(blank=True, help_text='Un nom courant du fichier', max_length=125, null=True)),
                ('slug', models.SlugField(blank=True, editable=False, max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('etat', models.IntegerField(choices=[(0, 'Conception'), (1, 'Partage'), (2, 'Publication'), (3, 'Archivage')], default=0)),
                ('validation', models.CharField(choices=[('AA', 'A approuver'), ('A', 'Approuvé'), ('AC', 'Approuvé et Commenté'), ('NA', 'Non Approuvé')], default='AA', max_length=2)),
                ('history_change_reason', models.TextField(null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical document',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identification', models.CharField(default=uuid.uuid4, editable=False, max_length=36)),
                ('fichier', models.FileField(max_length=255, upload_to=rudi.models.get_doc_filename, verbose_name='Document')),
                ('nom', models.CharField(blank=True, help_text='Un nom courant du fichier', max_length=125, null=True)),
                ('slug', models.SlugField(blank=True, editable=False, max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('etat', models.IntegerField(choices=[(0, 'Conception'), (1, 'Partage'), (2, 'Publication'), (3, 'Archivage')], default=0)),
                ('validation', models.CharField(choices=[('AA', 'A approuver'), ('A', 'Approuvé'), ('AC', 'Approuvé et Commenté'), ('NA', 'Non Approuvé')], default='AA', max_length=2)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='Une liste de mots-clés séparés par une virgule, en minuscule', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Mots-clés')),
            ],
        ),
    ]
