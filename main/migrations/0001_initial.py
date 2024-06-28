# Generated by Django 5.0.6 on 2024-06-28 20:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdministratorTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choosing', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='AppealToStudents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('text', models.TextField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=20)),
                ('content', models.TextField(blank=True, max_length=200)),
                ('images', models.ImageField(upload_to='gallery_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Graduates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('sourname', models.CharField(max_length=25)),
                ('year', models.PositiveIntegerField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='NameOfGrades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choosing', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='NamesOfOlympia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choosing', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('image', models.ImageField(upload_to='news_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OurAchievements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('image', models.ImageField(upload_to='achievements_images/')),
            ],
        ),
        migrations.CreateModel(
            name='SuccessfulStudents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='successful_students/')),
                ('content', models.TextField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teachers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('surname', models.CharField(max_length=20)),
                ('experience', models.CharField(choices=[('Год', '1'), ('От пяти лет', '5+'), ('От десяти лет', '10+')], max_length=50)),
                ('subject', models.CharField(max_length=20)),
                ('education', models.CharField(blank=True, max_length=200)),
                ('successes', models.CharField(blank=True, max_length=200)),
                ('image', models.ImageField(upload_to='teachers_images/')),
            ],
        ),
        migrations.CreateModel(
            name='ThanksNoteFromGraduates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('text', models.TextField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ThanksNoteFromStudents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('text', models.TextField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('sourname', models.CharField(max_length=25)),
                ('grade', models.CharField(choices=[('fifth', '5'), ('sixth', '6'), ('seventh', '7'), ('eighth', '8'), ('ninth', '9'), ('tenth', '10'), ('eleventh', '11')], max_length=50)),
                ('administrator_status', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='main.administratortypes')),
                ('name_of_grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.nameofgrades')),
                ('olympian_status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.namesofolympia')),
            ],
        ),
        migrations.CreateModel(
            name='Olympians',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.students')),
            ],
        ),
    ]
