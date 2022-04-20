from django.shortcuts import render
from django.urls import reverse
from main.models import User, Collection, Landmark

from django.db.models import Count

# Create your views here.


def collection_mypage(request):

    visited_landmark = Collection.objects.filter(user_id= request.session['id'])
    collection_cnt = len(visited_landmark)
    total = len(Landmark.objects.all())
    progress = int((collection_cnt/total)*100)
    return render(request, '../templates/collection/collection_mypage.html', context={'progress' : progress })

def collection_ranking(request):
    total = len(Landmark.objects.all())
    rank = Collection.objects.values('user_id').annotate(dcount=Count('user_id'))
    user_rank = []
    for i in rank:
        tmp = [list(i.values())[0], list(i.values())[1]]
        tmp_user = User.objects.get(id=list(i.values())[0]).username
        tmp_dict = {}
        tmp_dict['username'] = tmp_user
        tmp_dict['progress'] = int((tmp[1]/total)*100)
        user_rank.append(tmp_dict)

    user_rank=sorted(user_rank, key=lambda x:x['progress'], reverse=True)

    return render(request, '../templates/collection/collection_ranking.html',{'rank':user_rank})


# def collection_ranking(request):
#     total = len(Landmark.objects.all())
#     rank = Collection.objects.values('user_id').annotate(dcount=Count('user_id'))
#     user_rank=[]
#     for i in rank:
#         tmp = [list(i.values())[0], list(i.values())[1]]
#         tmp_user = User.objects.get(id=list(i.values())[0]).username
#         user_rank.append([tmp_user,int((tmp[1]/total)*100)])

#     user_rank.sort(key=lambda x:x[1])

#     return render(request, '../templates/collection/collection_ranking.html',{'rank':user_rank})

