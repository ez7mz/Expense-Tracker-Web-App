# Generated by Django 4.1 on 2022-08-23 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_alter_transaction_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-date']},
        ),
    ]