# Generated by Django 4.2.3 on 2023-07-26 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_profile_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='relationship_status',
            field=models.CharField(choices=[('single', 'single'), ('married', 'married')], default='none', max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='work',
            field=models.CharField(default='unemployed', max_length=200),
        ),
    ]
