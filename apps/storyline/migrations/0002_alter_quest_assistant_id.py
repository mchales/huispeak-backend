# Generated by Django 4.2.15 on 2024-10-15 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storyline', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quest',
            name='assistant_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
