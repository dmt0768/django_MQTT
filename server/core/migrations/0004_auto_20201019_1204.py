# Generated by Django 3.1.2 on 2020-10-19 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_messages_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topics',
            name='topic',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
