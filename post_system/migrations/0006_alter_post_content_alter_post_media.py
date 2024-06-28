# Generated by Django 5.0.6 on 2024-06-22 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_system', '0005_alter_post_media'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='media',
            field=models.FileField(default=None, upload_to='post_media/'),
            preserve_default=False,
        ),
    ]