# Generated by Django 5.0.6 on 2024-07-19 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_confirmeddonation_comment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='confirmeddonation',
            name='comment',
        ),
    ]
