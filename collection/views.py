from re import A
from django import conf
from django.shortcuts import render
from django.urls import reverse
from regex import B
from main.models import User, Collection, Landmark, Locations, Gallery
import os
from django.db.models import Count
from PIL import Image
import yolov5
from yolov5 import detect
from django.utils.timezone import now
from django.utils import timezone
from django.contrib import messages
# Create your views here.


# S3 이미지 업로드
import boto3
from config.settings import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,ALLOWED_HOSTS
import shutil



def collection_mypage(request):
    print("#############ALLOWED_HOSTS############## : ",ALLOWED_HOSTS)
    # progress bar
    print("request.user.is_authenticated : ",request.user.is_authenticated)
    if request.user.is_authenticated==True:
        ui = request.session['id']
        visited_landmark = Collection.objects.filter(user_id= ui)
        collection_cnt = len(visited_landmark)
        total = len(Landmark.objects.all())
        progress = int((collection_cnt/total)*100)

        #map
        test_dict = map(visited_landmark=visited_landmark,progress=progress)
        
        return render(request, '../templates/collection/collection_mypage.html', test_dict)
    else:
        messages.add_message(request, messages.INFO, '접근 권한이 없습니다')
        return render(request,'../templates/collection/collection_mypage.html')


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


def collection_update(request):

    ui = request.session['id']
    visited_landmark = Collection.objects.filter(user_id= ui)
    collection_cnt = len(visited_landmark)
    total = len(Landmark.objects.all())
    progress = int((collection_cnt/total)*100)

    # 카메라로 찍은 이미지 경로 설정
    path  = os.getcwd() # C:\Users\User\Desktop\potomable\git적용\Photo_Marble

    # 카메라 촬영 이미지 준비
    img = request.FILES['camcorder']
    img_name = img
    img = Image.open(img)
    time = timezone.now()
    
    #이미지 회전하기 90도 --> 핸드폰으로 찍으면 왼쪽으로 90회전 해서 나옴
    deg_image = img.transpose(Image.ROTATE_270)
    img = deg_image.save(path+'/collection/data/images/test.jpg')
    print("################# img_name : ",img_name)
    # yolo 실행
    conf=0.4
    detect.run(
            conf_thres=conf,
            source=path +'/collection/data/images',
            weights=path + '/collection/best.pt',
            name=path + '/collection/detect/result',
            line_thickness=20,
            save_txt=True,
            save_conf=True,
            exist_ok=True)

    # 추론 txt파일
    directoy_list = os.listdir(path + "/collection/detect/result/labels/")

    # 추론 txt파일 읽기 및 라벨 confidence값 불러오기
    f = open(path + "/collection/detect/result/labels/" + directoy_list[0], 'r')
    Annotate = f.readlines()[0].split()
    label=Annotate[0]
    confidence = Annotate[5]

    f.close()
    # UI에서 이미지가 너무 커서 이미지 크기 재 조정
    image = Image.open(path + "/collection/detect/result/"+'test.jpg')
    resize_image = image.resize((256,256))
    resize_image.save(path + "/collection/detect/result/"+'test.jpg')

    # s3에 업로드 할 이미지
    data = open(path + "/collection/detect/result/"+'test.jpg' , 'rb')

    # save results : S3로 업로드
    s3_url = "https://photomarble.s3.ap-northeast-2.amazonaws.com/yolo/"+ str(img_name)
    s3r = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3r.Bucket('photomarble').put_object( Key='yolo/'+str(img_name), Body=data, ContentType='jpg')
    data.close()

    # 해당 결과 파일 삭제
    del_path = path + "/collection/detect/result/"
    shutil.rmtree(del_path)

    # DB에 landmark ID, S3 URL 저장 
    user_id = request.session['id']
    colletion_idx = len(Collection.objects.all())+1 #나중에 컬렉션 id따서 +1 하는 방향으로(get)
    landmark_id = label
    time = timezone.now()
    try:
         # Collection 모델 업데이트
        Collection.objects.create(
            collection_id=colletion_idx , 
            is_visited=1, 
            date=time , 
            updated_at=time, 
            user_id=user_id, 
            landmark_id=landmark_id,
            s3_url=s3_url)

        # landmark == label
        # user_id == request.session['id']
        print("################## label : ",label)
        
        # collection_db = Collection.objects.get(s3_url=s3_url)

        
        # s3_url = collection_db.s3_url


        return render(request, '../templates/collection/collection_update.html',context={"s3_url":s3_url})
       

    except :
        print("이미 인증한 랜드마크입니다.")

        return render(request, '../templates/collection/collection_update.html')

        
    
def map(visited_landmark,progress):

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

    test_dict={}

    for i in range(0, 25):
        test_dict['s{}'.format(i+1)]= data_list[i]
        
    test_dict['progress'] = progress


    return test_dict