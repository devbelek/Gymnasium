# Generated by Django 5.0.6 on 2024-07-07 22:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_nameofgrades_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gimnasiumclass',
            name='student',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='main.students', verbose_name='Ученик'),
        ),
    ]
