from datetime import datetime, timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from main.validators import validate_no_special_characters


class User(AbstractUser):
    nickname = models.CharField(max_length=15, unique=True, null=True, validators=[validate_no_special_characters])
    profile_photo = models.CharField(max_length=300)
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
    date = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='user_id')
    landmark = models.ForeignKey('Landmark', models.DO_NOTHING, db_column='landmark_id')

    class Meta:
        # managed = False
        db_table = 'Collections'


class Gallery(models.Model):
    gallery_id = models.AutoField(primary_key=True)
    category_id = models.IntegerField()
    photo_url = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='user_id')
    landmark = models.ForeignKey('Landmark', models.DO_NOTHING, db_column='landmark_id', default='')
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


# 댓글 작성일 표시 형식 변경

class Free(models.Model):
    @property
    def created_string(self):
        time = datetime.now() - self.updated_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now().date() - self.updated_at.date()
            return str(time.days) + '일 전'
        else:
            return False

class Comment(models.Model):
    # 댓글 작성이 표시 형식 변경
    @property
    def created_string(self):
        time = datetime.now() - self.updated_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now().date() - self.updated_at.date()
            return str(time.days) + '일 전'
        else:
            return False

    comment_id = models.AutoField(primary_key=True)
    content = models.TextField()
    updated_at = models.DateTimeField()
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
