# Generated by Django 5.0.6 on 2024-07-03 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_system', '0004_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars'),
        ),
    ]