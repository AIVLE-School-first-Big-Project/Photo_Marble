from asyncio.windows_events import NULL
from tokenize import blank_re
from distutils.command.upload import upload
from django.shortcuts import render, redirect, get_object_or_404
from main.models import Gallery, Like, Comment, User, Landmark
from rest_framework.views import APIView
from django.utils import timezone
# from .forms import CommentForm
from django.utils import timezone
from datetime import datetime

def gallery(request):
    l_id = request.POST.get('landmark')
    c_id = request.POST.get('category')
    print(c_id)
    galleries = Gallery.objects.all()
    print(list(galleries)[0])
    landmarks = Landmark.objects.all()
    
    if request.method == 'POST':
        # 업로드 된 파일 저장
        # upload_file = request.FILES.get('file')

        # name = upload_file.name

        # with open(name, 'wb') as file:
        #     for chunk in upload_file.chunks():
        #         file.write(chunk)

        # 사진 필터링
        if (l_id is None and c_id is None)  or (l_id == '0' and c_id == '0'):
            galleries = Gallery.objects.all()
        elif l_id == '0' and c_id is not None:
            galleries = Gallery.objects.filter(category_id=c_id)
        elif l_id is not None and c_id == '0':
            galleries = Gallery.objects.filter(landmark_id=l_id)
        else:
            galleries = Gallery.objects.filter(landmark_id = l_id, category_id = c_id)
    content = {"datas" : galleries, "landmarks" : landmarks}

    return render(request, "../templates/gallery/gallery.html" , context= content)

def detail(request, id):
    user_id = request.session['id']
    galleries = Gallery.objects.get(gallery_id = id)
    upload_user = galleries.user_id
    profile_photo=User.objects.get(id=upload_user).profile_photo
    uploader= User.objects.get(id=upload_user).nickname
    likes = Like.objects.filter(gallery_id = id)
    
    if request.method == 'POST':
        comment = Comment()
        comment.content = request.POST.get('comment_textbox')
        if comment.content == '':
            comments = Comment.objects.filter(gallery_id=id)
            content = {"datas" : galleries, "len_likes": len(likes), "likes": likes, "comments":comments}
            return render(request, '../templates/gallery/detail.html', context=content)
        comment.user = User(id = user_id)
        comment.gallery = Gallery(gallery_id = id)
        comment.updated_at = timezone.now()
        comment.save()

    comments = Comment.objects.filter(gallery_id=id)
        
    content = {"datas" : galleries, "len_likes": len(likes), "likes": likes, "comments":comments, "my_id": user_id}
    return render(request, '../templates/gallery/detail.html', context=content)

def comment_delete(request, g_id, c_id):
    comment = get_object_or_404(Comment, pk=c_id)
    comment.delete()

    return redirect('detail2',id=g_id)

    
    
    
    


    
