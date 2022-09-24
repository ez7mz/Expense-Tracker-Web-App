# Generated by Django 4.1 on 2022-08-22 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0002_alter_user_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='balance',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='expense',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='income',
            field=models.FloatField(default=0),
        ),
    ]