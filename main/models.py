from django.db import models


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Gallery(models.Model):
    images = models.ImageField(upload_to='gallery_images/',blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Graduates(models.Model):
    image = models.ImageField(upload_to='graduate_images/',blank=False)
    updated_at = models.DateTimeField(auto_now=True)


class OurAchievements(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='achievements_images/', blank=False)


class Students(models.Model):
    name = models.CharField(max_length=20)


class Teachers(models.Model):
    Experience = (
        ('Год', '1'),
        ('От пяти лет', '5+'),
        ('От десяти лет', '10+'),
    )
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    experience = models.CharField(max_length=50, choices=Experience)
    subject = models.CharField(max_length=20)
    image = models.ImageField(upload_to='teachers_images/', blank=False)