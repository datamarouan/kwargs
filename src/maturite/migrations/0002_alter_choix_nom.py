# Generated by Django 3.2.12 on 2022-06-08 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maturite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choix',
            name='nom',
            field=models.CharField(max_length=255),
        ),
    ]