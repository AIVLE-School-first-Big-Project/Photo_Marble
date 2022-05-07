from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from main.validators import validate_no_special_characters


class User(AbstractUser):
    nickname = models.CharField(max_length=15, unique=True, null=True, validators=[validate_no_special_characters])
    profile_s3_url = models.CharField(max_length=400, default="https://photomarble.s3.ap-northeast-2.amazonaws.com/profile/blank-profile.png")
    profile_photo = models.ImageField(upload_to='profile', default="../static/main/images/balnk-profile.png")

    def __str__(self):
        return self.email


class Landmark(models.Model):
    landmark_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    x = models.FloatField()
    y = models.FloatField()
    area = models.CharField(max_length=50)

    class Meta:
        db_table = 'Landmark'


class Collection(models.Model):
    collection_id = models.AutoField(primary_key=True)
    is_visited = models.BooleanField()
    date = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey('User', db_column='user_id', on_delete=models.CASCADE)
    landmark = models.ForeignKey('Landmark', db_column='landmark_id', on_delete=models.CASCADE)
    s3_url = models.CharField(max_length=400, null=True)

    class Meta:
        db_table = 'Collections'


class Gallery(models.Model):
    gallery_id = models.AutoField(primary_key=True)
    category_id = models.IntegerField()
    photo_url = models.ImageField(upload_to='gallery')
    s3_url = models.CharField(max_length=400)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('User', db_column='user_id', on_delete=models.CASCADE)
    landmark = models.ForeignKey('Landmark', db_column='landmark_id', default='', on_delete=models.CASCADE)
    like_users = models.ManyToManyField(User, related_name='like_articles')
    latitude = models.DecimalField(max_digits=18, decimal_places=10, null=True)
    longitude = models.DecimalField(max_digits=18, decimal_places=10, null=True)
    created_at = models.DateTimeField(null=True)

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

    class Meta:
        db_table = 'Gallery'


class Photoguide(models.Model):
    photoguide_id = models.AutoField(primary_key=True)
    photo_url = models.CharField(max_length=100)
    vector = models.TextField()
    landmark = models.ForeignKey('Landmark', db_column='landmark_id', on_delete=models.CASCADE)

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
    user = models.ForeignKey('User', db_column='user_id', on_delete=models.CASCADE)
    gallery = models.ForeignKey('Gallery', db_column='gallery_id', on_delete=models.CASCADE)

    class Meta:
        # managed = False
        db_table = 'Comment'


class Like(models.Model):
    like_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', db_column='user_id', on_delete=models.CASCADE)
    gallery = models.ForeignKey('Gallery', db_column='gallery_id', on_delete=models.CASCADE)

    class Meta:
        # managed = False
        db_table = 'Like'


class Locations(models.Model):
    location_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        # managed = False
        db_table = 'Locations'
