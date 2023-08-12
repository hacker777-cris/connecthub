# Generated by Django 4.2.3 on 2023-08-12 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_remove_profile_following_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='base.profile'),
        ),
    ]