# Generated by Django 4.2.15 on 2024-11-29 05:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storyline', '0014_character_quest_character'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quest',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quests', to='storyline.character'),
        ),
    ]
