from asyncio.windows_events import NULL
from django.shortcuts import render, redirect, get_object_or_404
from main.models import Gallery, Like, Comment
from rest_framework.views import APIView
# from .forms import CommentForm
# from django import timezone

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
    # user_id = request.session['id']
    
    galleries = Gallery.objects.filter(gallery_id = id)

    likes = Like.objects.filter(gallery_id = id)

    #liked_cnt = len(likes)
    content = {"datas" : galleries, "likes": likes}
    print(content)
    return render(request, '../templates/gallery/detail.html', context = content)
    
    
    
    


    
