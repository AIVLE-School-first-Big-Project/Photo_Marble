from asyncio.windows_events import NULL
from django.shortcuts import render, redirect, get_object_or_404
from gallery.forms import CommentForm
from main.models import Gallery, Like, Comment, User
from rest_framework.views import APIView
# from .forms import CommentForm
from django.utils import *

def gallery(request):
    l_id = request.POST.get('landmark')
    c_id = request.POST.get('category')
    galleries = Gallery.objects.all()
    print(list(galleries)[0])

    if request.method == 'POST':
        if (l_id is None and c_id is None)  or (l_id == '0' and c_id == '0'):
            galleries = Gallery.objects.all()

        elif l_id == '0' and c_id is not None:
            galleries = Gallery.objects.filter(category_id=c_id)
        elif l_id is not None and c_id == '0':
            galleries = Gallery.objects.filter(landmark_id=l_id)
        else:
            galleries = Gallery.objects.filter(landmark_id = l_id, category_id = c_id)
    content = {"datas" : galleries}

    return render(request, "../templates/gallery/gallery.html" , context= content)

def detail(request, id):
    user_id = request.session['id']
    galleries = Gallery.objects.filter(gallery_id = id)

    likes = Like.objects.filter(gallery_id = id)
    
    if request.method == 'POST':
        comment = Comment()
        comment.content = request.POST.get('comment_textbox')
        comment.user = User(id = user_id)
        comment.gallery = Gallery(gallery_id = id)
        comment.updated_at = timezone.now()
        comment.save()

    comments = Comment.objects.filter(gallery_id=id)
    
    # User.username(id = comments.user_id)
    # for i in comments:
    #     print(i.user_id)

    content = {"datas" : galleries, "len_likes": len(likes), "likes": likes, "comments":comments}
    return render(request, '../templates/gallery/detail.html', context=content)



    
    
    
    


    
