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
    for i in range(1,26):
        dict_key = 's'+str(i)
        if dict_key in area_id:
            area_list.append('area_true')
        else:
            area_list.append('area_false')


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
                                                                                        's25':area_list[24]})


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

