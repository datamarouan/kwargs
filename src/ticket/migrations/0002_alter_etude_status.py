# Generated by Django 3.2.12 on 2022-05-21 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etude',
            name='status',
            field=models.IntegerField(choices=[(1, 'Stuck'), (2, 'Working'), (3, 'Done')], default=1),
        ),
    ]
