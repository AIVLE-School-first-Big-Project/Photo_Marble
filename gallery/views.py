from asyncio.windows_events import NULL
from django.shortcuts import render, redirect, get_object_or_404
from .models import Gallery, Like, Comment
from rest_framework.views import APIView

def select(request):
    c_id = request.GET.get('category')
    print(type(c_id))
    if c_id is None or c_id == '0':
        galleries = Gallery.objects.all()
    else:
        galleries = Gallery.objects.filter(categoryId = c_id)
    content = {"datas" : galleries}
    return render(request, "../templates/gallery/select.html" , context= content)

class Detail(APIView):
    def get(self, request, id):
        print(id)
        galleries = Gallery.objects.filter(galleryId = id)
        likes = Like.objects.filter(gallery_id = id)
        print(likes)
        #liked_cnt = len(likes)
        content = {"datas" : galleries, "likes": likes}
        
        return render(request, '../templates/gallery/detail.html', context = content)
