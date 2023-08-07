# Generated by Django 4.2.3 on 2023-08-02 13:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0009_follower'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='follower',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='follower',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='follower',
            name='follower',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='base.profile'),
        ),
        migrations.RemoveField(
            model_name='follower',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='follower',
            name='following',
        ),
        migrations.AddField(
            model_name='follower',
            name='following',
            field=models.ManyToManyField(related_name='following', to='base.profile'),
        ),
    ]
