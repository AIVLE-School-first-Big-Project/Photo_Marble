
import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from main.validators import validate_no_special_characters


class User(AbstractUser):
    nickname = models.CharField(max_length=15, unique=True, null=True, validators=[validate_no_special_characters])

    def __str__(self):
        return self.email

class Landmark(models.Model):
    lanmark_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    x = models.FloatField()
    y = models.FloatField()
    area = models.CharField(max_length=50)

    class Meta:
        # managed = False
        db_table = 'Landmark'


class Collection(models.Model):
    collection_id = models.AutoField(primary_key=True)
    is_visited = models.BooleanField()
    date = models.DateField()
    updated_at = models.DateField()
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='user_id')
    landmark = models.ForeignKey('Landmark', models.DO_NOTHING, db_column='landmark_id')

    class Meta:
        # managed = False
        db_table = 'Collections'


class Gallery(models.Model):
    gallery_id = models.AutoField(primary_key=True)
    category_id = models.IntegerField()
    photo_url = models.CharField(max_length=200)
    updated_at = models.DateField()
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='user_id')
    landmark = models.ForeignKey('Landmark', models.DO_NOTHING, db_column='landmark_id')
    class Meta:
        db_table = 'Gallery'


class Photoguide(models.Model):
    photoguide_id = models.AutoField(primary_key=True)
    photo_url = models.CharField(max_length=100)
    vector = models.TextField()
    landmark = models.ForeignKey('Landmark', models.DO_NOTHING, db_column='landmark_id')

    class Meta:
        # managed = False
        db_table = 'Photoguide'

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    class Meta:
        # managed = False
        db_table = 'Category'

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    content = models.TextField()
    updated_at = models.DateField()
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='user_id')
    gallery = models.ForeignKey('Gallery', models.DO_NOTHING, db_column='gallery_id')
    class Meta:
        # managed = False
        db_table = 'Comment'

class Like(models.Model):
    like_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='user_id')
    gallery = models.ForeignKey('Gallery', models.DO_NOTHING, db_column='gallery_id')
    class Meta:
        # managed = False
        db_table = 'Like'



class Locations(models.Model):
    location_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)


    class Meta:
        # managed = False
        db_table = 'Locations'
