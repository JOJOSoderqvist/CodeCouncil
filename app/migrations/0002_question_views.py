# Generated by Django 4.2.11 on 2024-04-07 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='views',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
