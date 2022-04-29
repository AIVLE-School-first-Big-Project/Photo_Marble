from asyncio.windows_events import NULL
from tokenize import blank_re
from distutils.command.upload import upload
from unicodedata import category
from django.shortcuts import render, redirect, get_object_or_404
from main.models import Gallery, Like, Comment, User, Landmark
from django.utils.timezone import now
from rest_framework.views import APIView
from django.utils import timezone
# from .forms import CommentForm
from django.utils import timezone
from datetime import datetime
from django.http import HttpResponse,JsonResponse
import json
from django.core import serializers
from django.core.paginator import *

def gallery(request):
    l_id = request.POST.get('landmark')
    c_id = request.POST.get('category')
    galleries = Gallery.objects.all()
    landmarks = Landmark.objects.all()

    # Pagination
    paginator = Paginator(galleries, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.method == 'POST':
        # 사진 필터링
        if (l_id is None and c_id is None)  or (l_id == '0' and c_id == '0'):
            galleries = Gallery.objects.all()
        elif l_id == '0' and c_id is not None:
            galleries = Gallery.objects.filter(category_id=c_id)
        elif l_id is not None and c_id == '0':
            galleries = Gallery.objects.filter(landmark_id=l_id)
        else:
            galleries = Gallery.objects.filter(landmark_id = l_id, category_id = c_id)
        
    content = {'page_obj':page_obj, "landmarks" : landmarks, 'datas':galleries}
    return render(request, "../templates/gallery/gallery.html" , context= content)

# Pagination

def load_more(request):
    offset = int(request.POST['offset'])
    limit = 4
    posts = Gallery.objects.all()[offset:offset + limit]
    totalData = Gallery.objects.count()
    data={}
    posts_json = serializers.serialize('json', posts)
    return JsonResponse(data={
        'posts':posts_json,
        'totalResult':totalData,
    })


def upload(request):
    if request.method == 'POST':
        user_id = request.session['id']
        gallery_idx = len(Gallery.objects.all())+1
        img = request.FILES['file']
        category = request.POST.get('category')
        landmark=request.POST.get('landmark')
        time = timezone.now()
        s3_url = "https://photomarble.s3.ap-northeast-2.amazonaws.com/gallery/"+ str(img)
        Gallery.objects.create(s3_url = s3_url, updated_at=time,category_id=category, landmark_id=landmark,user_id=user_id,photo_url=img)
    return redirect('http://127.0.0.1:8000/gallery/')


def detail(request, id):
    user_id = request.session['id']
    galleries = Gallery.objects.get(gallery_id = id)
    upload_user = galleries.user_id
    profile_photo=User.objects.get(id=upload_user).profile_s3_url
    uploader= User.objects.get(id=upload_user).nickname
    #likes = Gallery.like_users.filter(gallery_id = id)
    print(galleries.like_users.count())

    if request.method == 'POST':
        comment = Comment()
        comment.content = request.POST.get('comment_textbox')
        if comment.content == '':
            comments = Comment.objects.filter(gallery_id=id)
            content = {"data" : galleries, "len_likes": galleries.like_users.count(), "likes": likes, "comments":comments,"uploader":uploader,"profile_photo":profile_photo,}
            return render(request, '../templates/gallery/detail.html', context=content)
        comment.user = User(id = user_id)
        comment.gallery = Gallery(gallery_id = id)
        comment.updated_at = timezone.now()
        comment.save()

        return redirect('detail2',id=id)

    comments = Comment.objects.filter(gallery_id=id)
        
    content = {"data" : galleries, "len_likes": galleries.like_users.count(), "likes": likes,"uploader":uploader,"profile_photo":profile_photo,"comments":comments, "my_id": user_id}
    return render(request, '../templates/gallery/detail.html', context=content)

def comment_delete(request, g_id, c_id):
    comment = get_object_or_404(Comment, pk=c_id)
    comment.delete()

    return redirect('detail2', id=g_id)

    

def likes(request):
    if request.is_ajax(): 
        gallery_id = request.GET['gallery_id']
        gallery = Gallery.objects.get(gallery_id=gallery_id) 
        user = request.user
        if gallery.like_users.filter(id = user.id).exists():
            print("yes")
            gallery.like_users.remove(user)
            message = "좋아요 취소"
        else:
            gallery.like_users.add(user)
            message = "좋아요"
            print("no")
        context = {'like_count' : gallery.like_users.count(),"message":message}
        return HttpResponse(json.dumps(context), content_type='application/json')    
    
def gallery_delete(request, g_id):
    gallery = get_object_or_404(Gallery, pk=g_id)
    gallery.delete()

    return redirect('gallery')
    

# def likes(request, id):
#     if request.user.is_authenticated:
#         gallery = get_object_or_404(Gallery, pk=id)
#         user_id = request.session['id']
     
#         if gallery.like_users.filter(id=user_id).exists():
#             gallery.like_users.remove(request.user)
#         else:
#             gallery.like_users.add(request.user)
      
#     user_id = request.session['id']
#     galleries = Gallery.objects.get(gallery_id = id)
#     upload_user = galleries.user_id
#     profile_photo=User.objects.get(id=upload_user).profile_s3_url
#     uploader= User.objects.get(id=upload_user).nickname
#     likes = Like.objects.filter(gallery_id = id)
#     comments = Comment.objects.filter(gallery_id=id)
#     content = {"data" : galleries, "len_likes": len(likes), "likes": likes,"uploader":uploader,"profile_photo":profile_photo,"comments":comments, "my_id": user_id}
#     return render(request, '../templates/gallery/detail.html', context=content)
    

    

# def likes(request, id):
#     if request.user.is_authenticated:
#         gallery = get_object_or_404(Gallery, pk=id)
#         user_id = request.session['id']
#         if Like.objects.filter(like_id=user_id).exists():
#             record = Like.objects.filter(like_id=user_id)
#             record.delete()
            
#         else:
#             Like.objects.create(user_id =user_id,gallery_id=id )
            
#         return redirect('http://127.0.0.1:8000/gallery/detail/1/')
#     return redirect('http://127.0.0.1:8000/gallery/detail/1/')
    
    
