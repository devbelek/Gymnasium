# Generated by Django 5.0.6 on 2024-07-03 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_alter_olympians_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='olympians',
            name='name',
        ),
    ]
