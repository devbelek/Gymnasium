# Generated by Django 5.0.6 on 2024-09-02 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secondary', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='namesofolympia',
            name='choosing_ky',
            field=models.CharField(max_length=20, null=True, unique=True, verbose_name='Название олимпиады'),
        ),
        migrations.AddField(
            model_name='namesofolympia',
            name='choosing_ru',
            field=models.CharField(max_length=20, null=True, unique=True, verbose_name='Название олимпиады'),
        ),
        migrations.AlterField(
            model_name='namesofolympia',
            name='choosing',
            field=models.CharField(max_length=20, unique=True, verbose_name='Название олимпиады'),
        ),
    ]
