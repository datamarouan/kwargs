# Generated by Django 3.2.12 on 2022-05-27 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projet', '0004_alter_tache_projet'),
    ]

    operations = [
        migrations.AddField(
            model_name='tache',
            name='date_butoir',
            field=models.DateField(blank=True, null=True),
        ),
    ]
