# Generated by Django 4.1 on 2022-08-26 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyseme', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anlysefile',
            name='file',
            field=models.FileField(upload_to=''),
        ),
    ]
