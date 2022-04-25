from asyncio.windows_events import NULL
from django.shortcuts import render, redirect, get_object_or_404
from main.models import Gallery, Like, Comment
from rest_framework.views import APIView

def select(request):
    c_id = request.POST.get('category')
    print(c_id)
    galleries = Gallery.objects.all()


    if request.method == 'POST':
        if c_id is None or c_id == '0':
            galleries = Gallery.objects.all()
        else:
            galleries = Gallery.objects.filter(category_id = c_id)
    content = {"datas" : galleries}

    return render(request, "../templates/gallery/select.html" , context= content)

def detail(request, id):
    print(id)
    galleries = Gallery.objects.filter(gallery_id = id)
    likes = Like.objects.filter(gallery_id = id)
    print(likes)
    #liked_cnt = len(likes)
    content = {"datas" : galleries, "likes": likes}
    
    return render(request, '../templates/gallery/detail.html', context = content)
