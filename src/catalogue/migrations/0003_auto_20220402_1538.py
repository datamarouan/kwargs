# Generated by Django 3.2.12 on 2022-04-02 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_auto_20220402_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kwgpostaladdress',
            name='latitude',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='kwgpostaladdress',
            name='longitude',
            field=models.FloatField(default=0),
        ),
    ]
