# Generated by Django 4.2.3 on 2023-08-02 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_alter_follower_unique_together_follower_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='follower_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
