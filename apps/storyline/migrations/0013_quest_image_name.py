# Generated by Django 4.2.15 on 2024-11-24 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storyline', '0012_remove_quest_objectives_objectives'),
    ]

    operations = [
        migrations.AddField(
            model_name='quest',
            name='image_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
