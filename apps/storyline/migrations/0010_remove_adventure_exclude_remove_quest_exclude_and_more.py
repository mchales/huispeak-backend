# Generated by Django 4.2.15 on 2024-10-17 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storyline', '0009_adventure_exclude_quest_exclude_story_exclude'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adventure',
            name='exclude',
        ),
        migrations.RemoveField(
            model_name='quest',
            name='exclude',
        ),
        migrations.RemoveField(
            model_name='story',
            name='exclude',
        ),
        migrations.AddField(
            model_name='adventure',
            name='include',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='quest',
            name='include',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='story',
            name='include',
            field=models.BooleanField(default=True),
        ),
    ]
