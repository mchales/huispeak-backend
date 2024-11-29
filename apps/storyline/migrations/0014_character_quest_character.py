# Generated by Django 4.2.15 on 2024-11-28 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storyline', '0013_quest_image_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('voice', models.CharField(choices=[('alloy', 'Alloy'), ('echo', 'Echo'), ('fable', 'Fable'), ('onyx', 'Onyx'), ('nova', 'Nova'), ('shimmer', 'Shimmer')], default='alloy', max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='quest',
            name='character',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quests', to='storyline.character'),
        ),
    ]
