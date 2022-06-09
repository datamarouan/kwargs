# Generated by Django 3.2.12 on 2022-06-08 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0001_initial'),
        ('rudi', '0001_initial'),
        ('projet', '0005_tache_docz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projet',
            name='docz',
            field=models.ManyToManyField(blank=True, null=True, related_name='documentation', to='rudi.Document'),
        ),
        migrations.AlterField(
            model_name='projet',
            name='localisation',
            field=models.ManyToManyField(blank=True, null=True, related_name='endroits', to='catalogue.GeoRefPostalAddress'),
        ),
        migrations.AlterField(
            model_name='tache',
            name='docz',
            field=models.ManyToManyField(blank=True, null=True, related_name='documents_lies', to='rudi.Document'),
        ),
    ]