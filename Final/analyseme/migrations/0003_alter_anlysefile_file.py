# Generated by Django 4.1 on 2022-08-26 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyseme', '0002_alter_anlysefile_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anlysefile',
            name='file',
            field=models.FileField(upload_to='Files_to_Analyse'),
        ),
    ]
