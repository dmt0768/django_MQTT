# Generated by Django 3.1.2 on 2020-10-19 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20201019_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='topic_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.topics'),
        ),
    ]