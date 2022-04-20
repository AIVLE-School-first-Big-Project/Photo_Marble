from django.db import models

# Create your models here.
class Gallery(models.Model):
    galleryId = models.IntegerField(primary_key=True)
    categoryId = models.IntegerField()
    photo = models.TextField()
    userId = models.IntegerField()
    updateAt = models.DateTimeField()
    createdAt = models.DateTimeField()

class Like(models.Model):
    like_id = models.IntegerField(primary_key=True)
    gallery_id = models.IntegerField()
    user_id = models.IntegerField()

class Comment(models.Model):
    comment_id = models.IntegerField(primary_key=True)
    content = models.TextField()
    updateAt = models.DateTimeField()
    gallery_id = models.IntegerField()
    user_id = models.IntegerField()