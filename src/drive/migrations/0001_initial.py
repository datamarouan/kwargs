# Generated by Django 3.2.12 on 2022-04-30 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import drive.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('identification', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('fichier', models.FileField(max_length=255, upload_to=drive.models.get_doc_filename, verbose_name='Document')),
                ('nom', models.CharField(blank=True, help_text='Un nom courant du fichier', max_length=125, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('etat', models.IntegerField(choices=[(0, 'Conception'), (1, 'Partage'), (2, 'Publication'), (3, 'Archivage')], default=0)),
                ('validation', models.CharField(choices=[('AA', 'A approuver'), ('A', 'Approuvé'), ('AC', 'Approuvé et Commenté'), ('NA', 'Non Approuvé')], default='AA', max_length=2)),
                ('created_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='drive_document_created', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='drive_document_modified', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
