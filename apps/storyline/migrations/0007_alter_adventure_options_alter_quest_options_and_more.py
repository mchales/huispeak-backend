# Generated by Django 4.2.15 on 2024-10-17 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storyline', '0006_alter_adventure_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adventure',
            options={'ordering': ['adventure_num']},
        ),
        migrations.AlterModelOptions(
            name='quest',
            options={'ordering': ['quest_num']},
        ),
        migrations.AlterModelOptions(
            name='story',
            options={'ordering': ['story_num']},
        ),
        migrations.RemoveField(
            model_name='adventure',
            name='next_node',
        ),
        migrations.RemoveField(
            model_name='adventure',
            name='prev_node',
        ),
        migrations.RemoveField(
            model_name='quest',
            name='next_node',
        ),
        migrations.RemoveField(
            model_name='quest',
            name='prev_node',
        ),
        migrations.RemoveField(
            model_name='story',
            name='next_node',
        ),
        migrations.RemoveField(
            model_name='story',
            name='prev_node',
        ),
    ]
