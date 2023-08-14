# Generated by Django 4.2.3 on 2023-08-14 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0025_alter_profile_relationship_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='work',
            field=models.CharField(max_length=200),
        ),
    ]