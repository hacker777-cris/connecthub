# Generated by Django 4.2.3 on 2023-08-14 08:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0023_remove_post_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='text',
        ),
    ]