# Generated by Django 5.0.6 on 2024-07-08 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='sender',
            new_name='user',
        ),
    ]
