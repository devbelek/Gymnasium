# Generated by Django 5.0.6 on 2024-07-03 15:30

import main.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_olympians_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='olympians',
            name='name',
            field=models.CharField(max_length=20, verbose_name=main.models.Students),
        ),
    ]
