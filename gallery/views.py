from django.shortcuts import render, redirect, get_object_or_404
from main.models import Gallery, Like, Comment, User, Landmark
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
import json
from django.core import *
from django.core.paginator import *
from django.core import serializers
from PIL import Image
from PIL.ExifTags import TAGS


# 갤러리 전체보기
# 랜드마크별 필터링, 페이지네이션
def gallery(request):
    l_id = request.POST.get('landmark')
    c_id = request.POST.get('category')
    galleries = Gallery.objects.all().order_by('-updated_at')
    landmarks = Landmark.objects.all()

    if request.method == 'POST':
        # 사진 필터링
        if (l_id is None and c_id is None) or (l_id == '0' and c_id == '0'):
            galleries = Gallery.objects.all().order_by('-updated_at')
        elif l_id == '0' and c_id is not None:
            galleries = Gallery.objects.filter(category_id=c_id).order_by('-updated_at')
        elif l_id is not None and c_id == '0':
            galleries = Gallery.objects.filter(landmark_id=l_id).order_by('-updated_at')
        else:
            galleries = Gallery.objects.filter(landmark_id=l_id, category_id=c_id).order_by('-updated_at')

    # Pagination
    paginator = Paginator(galleries, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    content = {'page_obj': page_obj, "landmarks": landmarks, 'galleries': galleries}

    return render(request, "../templates/gallery/gallery.html", context=content)


# 페이지네이션
# [더 보기] 버튼으로 AJAX 통신하여 불러올 수 있도록.
def load_more(request):
    offset = int(request.POST['offset'])
    limit = 4
    posts = Gallery.objects.all()[offset:offset + limit]
    totalData = Gallery.objects.count()
    posts_json = serializers.serialize('json', posts)
    return JsonResponse(data={
        'posts': posts_json,
        'totalResult': totalData,
    })


# 갤러리 업로드
def upload(request):
    if request.method == 'POST':
        user_id = request.session['id']
        img = request.FILES['file']
        category = request.POST.get('category')
        landmark = request.POST.get('landmark')
        time = timezone.now()
        s3_url = "https://photomarble.s3.ap-northeast-2.amazonaws.com/gallery/" + str(img)

        # 사진 메타데이터 (시간, 위치) 저장
        temp_img = Image.open(img)
        img_info = temp_img._getexif()
        taglabel = {}
        if img_info is None:
            img_info = {}

        for tag, value in img_info.items():
            decoded = TAGS.get(tag, tag)
            taglabel[decoded] = value

        if 'GPSInfo' in taglabel.keys():
            exifGPS = taglabel['GPSInfo']
            latData, lonData = exifGPS[2], exifGPS[4]

            # 도, 분, 초
            latDeg, latMin, latSec = latData[0], latData[1], latData[2]
            lonDeg, lonMin, lonSec = lonData[0], lonData[1], lonData[2]

            # 위도 계산
            latitude = (latDeg + (latMin + latSec / 60.0) / 60.0)

            # 경도 계산
            longitude = (lonDeg + (lonMin + lonSec / 60.0) / 60.0)

            # 사진이 생성된 날짜 (created_at)
            taglabel['DateTimeOriginal']
            tmp_date = taglabel['DateTimeOriginal'][:10].replace(':', '-')
            tmp_time = taglabel['DateTimeOriginal'][10:]
            created_at = tmp_date + tmp_time

        # 사진 메타데이터 (시간, 위치) 저장
        else:
            latitude = 0
            longitude = 0
            created_at = time

        Gallery.objects.create(
            s3_url=s3_url,
            updated_at=time,
            category_id=category,
            landmark_id=landmark,
            user_id=user_id,
            photo_url=img,
            latitude=latitude,
            longitude=longitude,
            created_at=created_at)

    return redirect('gallery')


# 사진 상세페이지 보기
# 댓글(CRUD), 좋아요(AJAX 통신) 기능
def detail(request, id):
    user_id = request.session['id']
    galleries = Gallery.objects.get(gallery_id=id)
    upload_user = galleries.user_id
    profile_photo = User.objects.get(id=upload_user).profile_s3_url
    uploader = User.objects.get(id=upload_user).nickname
    likes = Like.objects.filter(gallery_id=id)

    if request.method == 'POST':
        comment = Comment()
        comment.content = request.POST.get('comment_textbox')
        if comment.content == '':
            comments = Comment.objects.filter(gallery_id=id)
            content = {
                "data": galleries,
                "len_likes": galleries.like_users.count(),
                "likes": likes, "comments": comments,
                "uploader": uploader,
                "profile_photo": profile_photo}

            return render(request, '../templates/gallery/detail.html', context=content)

        comment.user = User(id=user_id)
        comment.gallery = Gallery(gallery_id=id)
        comment.updated_at = timezone.now()
        comment.save()

        return redirect('detail2', id=id)

    comments = Comment.objects.filter(gallery_id=id)
    content = {
        "data": galleries,
        "len_likes": galleries.like_users.count(),
        "likes": likes,
        "uploader": uploader,
        "profile_photo": profile_photo,
        "comments": comments,
        "my_id": user_id}

    return render(request, '../templates/gallery/detail.html', context=content)


# 댓글 삭제
def comment_delete(request, g_id, c_id):
    comment = get_object_or_404(Comment, pk=c_id)
    comment.delete()

    return redirect('detail2', id=g_id)


# 좋아요 기능
def likes(request):
    if request.is_ajax():
        gallery_id = request.GET['gallery_id']
        gallery = Gallery.objects.get(gallery_id=gallery_id)
        user = request.user

        # 유저가 좋아요를 했다가 취소하기
        if gallery.like_users.filter(id=user.id).exists():
            gallery.like_users.remove(user)
            message = "좋아요 취소"

        else:
            gallery.like_users.add(user)
            message = "좋아요"

        context = {'like_count': gallery.like_users.count(), "message": message}
        return HttpResponse(json.dumps(context), content_type='application/json')


# 갤러리 삭제
def gallery_delete(request, g_id):
    gallery = get_object_or_404(Gallery, pk=g_id)
    gallery.delete()

    return redirect('gallery')
