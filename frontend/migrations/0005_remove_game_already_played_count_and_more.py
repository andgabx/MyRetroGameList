# Generated by Django 5.1.1 on 2024-09-28 03:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0004_game_favorite_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='already_played_count',
        ),
        migrations.RemoveField(
            model_name='game',
            name='favorite_count',
        ),
        migrations.RemoveField(
            model_name='game',
            name='like_count',
        ),
        migrations.RemoveField(
            model_name='game',
            name='playing_count',
        ),
        migrations.RemoveField(
            model_name='game',
            name='to_play_count',
        ),
    ]
