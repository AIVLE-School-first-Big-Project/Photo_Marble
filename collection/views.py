from django.shortcuts import render
from django.urls import reverse
from main.models import User, Collection, Landmark, Locations

from django.db.models import Count

# Create your views here.


def collection_mypage(request):
    # progress bar
    ui = request.session['id']
    visited_landmark = Collection.objects.filter(user_id= ui)
    collection_cnt = len(visited_landmark)
    total = len(Landmark.objects.all())
    progress = int((collection_cnt/total)*100)

    # map
    area_id=[]
    for i in visited_landmark:
        l_d=i.landmark_id
        land=Landmark.objects.get(lanmark_id= l_d)
        area_name=land.area
        land=Locations.objects.get(name= area_name)
        area_id.append('s'+str(land.location_id))
    print(area_id)

    return render(request, '../templates/collection/collection_mypage.html', context={'progress' : progress,
                                                                                        'area_id' : area_id,
     })

def collection_ranking(request):
    total = len(Landmark.objects.all())
    rank = list(Collection.objects.values('user_id').annotate(dcount=Count('user_id')))
    rank = sorted(rank, key=lambda x:x['dcount'], reverse=True)
    user_rank = []
    flag = False
    for idx, i in enumerate(rank):
        if idx < 2: # 몇등까지 보여줄지
            tmp = [list(i.values())[0], list(i.values())[1]]
            tmp_user = User.objects.get(id=tmp[0]).username
            tmp_dict = {}
            tmp_dict['username'] = tmp_user
            tmp_dict['progress'] = int((tmp[1]/total)*100)
            if(tmp[0]==request.session['id']):
                tmp_dict['isUser'] = True
                flag = True
            else:
                tmp_dict['isUser'] = False

            user_rank.append(tmp_dict)
       
        else:
            break
    if flag == False:
        my_rank = {'username':User.objects.get(id=request.session['id']).username,
                        'progress':int((len(Collection.objects.filter(user_id=request.session['id']))/total)*100),
                        'isUser':True}
    else:
        my_rank = False

    return render(request, '../templates/collection/collection_ranking.html',{'rank':user_rank,'my_rank':my_rank, 'flag':flag})


def maps(request):
    return render(request, "../templates/collection/collection_mypage.html")
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

