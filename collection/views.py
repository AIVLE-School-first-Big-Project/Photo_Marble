from re import A
from django.shortcuts import render,redirect
from django.urls import reverse
from main.models import User, Collection, Landmark, Locations, Gallery

from django.db.models import Count
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
# Create your views here.

def collection_mypage(request):
    # progress bar
    print("request.user.is_authenticated : ",request.user.is_authenticated)
    if request.user.is_authenticated==True:
        ui = request.session['id']
        visited_landmark = Collection.objects.filter(user_id= ui)
        collection_cnt = len(visited_landmark)
        total = len(Landmark.objects.all())
        progress = int((collection_cnt/total)*100)
        
        # map
        area_id=[]
        for i in visited_landmark:
            l_d=i.landmark_id
            land=Landmark.objects.get(landmark_id= l_d)
            area_name=land.area
            land=Locations.objects.get(name= area_name)
            area_id.append('s'+str(land.location_id))

    
        data_list=[]
        for i in range(1,26):
            data_dict={}
            dict_key = 's'+str(i)
            if dict_key in area_id:

                data_dict['area']='area_true'
                data_dict['marker']='marker'
                data_list.append(data_dict)
            else:

                data_dict['area']='area_false'
                data_dict['marker']='empty'
                data_list.append(data_dict)
        # svg 태그 안에서 foor loop가 불가능해 우선은 하드코딩 (25개 개별로 전달) 추후에 수정 예정 ....
        # import json
        # a_list=json.dumps(area_list)
        test_dict={}
        # model = yolov5.load('best.pt')
        # img = 'data/seock.jpg'
        # results = model(img)
        # results.save(save_dir='results/')
        # test_dict["result"] = results

        for i in range(0, 25):
            test_dict['s{}'.format(i+1)]= data_list[i]
        
        test_dict['progress'] = progress
        
        # if request.method == "POST":
        #     loc_id = request.POST.get('loc_id')
        #     loc=Locations.objects.get(location_id = loc_id)
        #     loc_name=loc.name
        #     lands_area=Landmark.objects.filter(area = loc_name)
        #     land_list=[]
        #     print(loc_id)
        #     for land in lands_area:
        #         land_list.append(land.landmark_id)
        #     my_galleries = Gallery.objects.filter(user=ui, landmark_id__in=land_list)
        #     print(my_galleries)
        #     test_dict["datas"] = my_galleries

        return render(request, '../templates/collection/collection_mypage.html', context=test_dict)
    else:
        messages.add_message(request, messages.INFO, '접근 권한이 없습니다')
        return render(request,'../templates/collection/collection_mypage.html')


def map_modal(request):
    
    area = Locations.objects.get(location_id=request.POST['location_id'][1:])

    landmarks  = Landmark.objects.filter(area=area.name)
    land_id_lilst = [l.landmark_id for l in landmarks]
    collection =  Collection.objects.filter(landmark_id__in=land_id_lilst,user_id=request.session['id'])
    coll_id_lilst = [l.landmark_id for l in collection]
    user_collection=  Landmark.objects.filter(landmark_id__in=coll_id_lilst)
    result  = [ i.name for i in user_collection]
    print(user_collection)
    #collection_db = Collection.objects.filter(user_id=request.session['id'], landmark_id=label)
    return JsonResponse(data={
        'landmarks':list(user_collection.values()),
 
    })



from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def my_gallery(request,loc_id):
    ui = request.session['id']
    loc=Locations.objects.get(location_id = loc_id)
    loc_name=loc.name
    lands_area=Landmark.objects.filter(area = loc_name)
    land_list=[]
    for land in lands_area:
        land_list.append(land.landmark_id)
    my_galleries = Gallery.objects.filter(user=ui, landmark_id__in=land_list)
    
    visited_lands = []

    for my_g in my_galleries:
        visited_lands.append(my_g.landmark_id)

    landset = list(set(visited_lands))

    lands_area = Landmark.objects.filter(area=loc_name, landmark_id__in=landset)
    
    content = {"datas" : my_galleries, "landmarks":lands_area}
    
    return render(request, "../templates/collection/my_gallery.html" , context= content)

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
        tmp_dict['profile_photo'] = user.profile_s3_url
        tmp_dict['rank'] = (i+1)
        tmp_dict['color'] = (i+1) %2 

        rank_list.append(tmp_dict)
    if len(rank_list)==1:
        rank_list.append(None)
        rank_list.append(None)
    elif len(rank_list)==2:
        rank_list.append(None)
    return render(request, '../templates/collection/collection_ranking.html',
                    {'first':rank_list[0], 'second':rank_list[1],'third':rank_list[2],'top4_7':rank_list[3:]})

