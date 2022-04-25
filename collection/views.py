from re import A
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

    area_list = []
    marker_list =[]
    for i in range(1,26):
        dict_key = 's'+str(i)
        if dict_key in area_id:
            area_list.append('area_true')
            marker_list.append('marker')
        else:
            area_list.append('area_false')
            marker_list.append('empty')
    print(marker_list)
    # svg 태그 안에서 foor loop가 불가능해 우선은 하드코딩 (25개 개별로 전달) 추후에 수정 예정 ....
    
    x_cal = 5
    y_cal = 5
    return render(request, '../templates/collection/collection_mypage.html', context={'progress' : progress,
                                                                                        's1':area_list[0],
                                                                                        's2':area_list[1],
                                                                                        's3':area_list[2],
                                                                                        's4':area_list[3],
                                                                                        's5':area_list[4],
                                                                                        's6':area_list[5],
                                                                                        's7':area_list[6],
                                                                                        's8':area_list[7],
                                                                                        's9':area_list[8],
                                                                                        's10':area_list[9],
                                                                                        's11':area_list[10],
                                                                                        's12':area_list[11],
                                                                                        's13':area_list[12],
                                                                                        's14':area_list[13],
                                                                                        's15':area_list[14],
                                                                                        's16':area_list[15],
                                                                                        's17':area_list[16], 
                                                                                        's18':area_list[17], 
                                                                                        's19':area_list[18], 
                                                                                        's20':area_list[19], 
                                                                                        's21':area_list[20], 
                                                                                        's22':area_list[21], 
                                                                                        's23':area_list[22], 
                                                                                        's24':area_list[23], 
                                                                                        's25':area_list[24],

                                                                                        'm1':marker_list[0],
                                                                                        'm2':marker_list[1],
                                                                                        'm3':marker_list[2],
                                                                                        'm4':marker_list[3],
                                                                                        'm5':marker_list[4],
                                                                                        'm6':marker_list[5],
                                                                                        'm7':marker_list[6],
                                                                                        'm8':marker_list[7],
                                                                                        'm9':marker_list[8],
                                                                                        'm10':marker_list[9],
                                                                                        'm11':marker_list[10],
                                                                                        'm12':marker_list[11],
                                                                                        'm13':marker_list[12],
                                                                                        'm14':marker_list[13],
                                                                                        'm15':marker_list[14],
                                                                                        'm16':marker_list[15],
                                                                                        'm17':marker_list[16],
                                                                                        'm18':marker_list[17],
                                                                                        'm19':marker_list[18],
                                                                                        'm20':marker_list[19],
                                                                                        'm21':marker_list[20],
                                                                                        'm22':marker_list[21],
                                                                                        'm23':marker_list[22],
                                                                                        'm24':marker_list[23],
                                                                                        'm25':marker_list[24],
                                                                                        'x_cal' : x_cal,
                                                                                        'y_cal' : y_cal}
                                                                                        )


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

def collection_ranking(request):
    
    rank = list(Collection.objects.values('user_id').annotate(dcount=Count('user_id')))
    rank = sorted(rank, key=lambda x:x['dcount'], reverse=True)
    rank_list = []
    if len(rank)<10:
        idx=len(rank)
    else:
        idx = 10
    for i in range(idx):
        user = User.objects.get(id=(rank[i]['user_id']))
       # user = User.objects.get(id=)
        tmp_dict={}
        tmp_dict['username'] = user.nickname
        tmp_dict['cnt'] = rank[i]['dcount']
        tmp_dict['profile_photo'] = user.profile_photo
        tmp_dict['rank'] = (i+1)
        tmp_dict['color'] = (i+1) %2 
        rank_list.append(tmp_dict)
    return render(request, '../templates/collection/collection_ranking.html',
                    {'first':rank_list[0], 'second':rank_list[1],'third':rank_list[2],'top4_7':rank_list[3:]})
