# Generated by Django 3.2.12 on 2022-04-30 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drive', '0005_auto_20220501_0102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaldocument',
            name='history_change_reason',
            field=models.TextField(null=True),
        ),
    ]