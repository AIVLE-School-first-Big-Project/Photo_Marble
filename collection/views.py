from django.shortcuts import render, redirect
from main.models import User, Collection, Landmark, Locations, Gallery
import os
from django.db.models import Count
from PIL import Image
from yolov5 import detect
from django.utils import timezone
from django.http import JsonResponse

# S3 이미지 업로드
import boto3
from config.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
import shutil

# API
from django.views.decorators.csrf import csrf_exempt


def collection_mypage(request):
    # progress bar
    if request.user.is_authenticated is True:
        ui = request.session['id']
        visited_landmark = Collection.objects.filter(user_id=ui)
        collection_cnt = len(visited_landmark)
        total = len(Landmark.objects.all())
        progress = int((collection_cnt / total) * 100)

        # map
        test_dict = map(visited_landmark=visited_landmark, progress=progress)
        return render(request, '../templates/collection/collection_mypage.html', test_dict)

    else:
        return render(request, '../templates/collection/collection_mypage.html')


@csrf_exempt
def my_gallery(request, loc_id):
    ui = request.session['id']
    landmark = Landmark.objects.get(landmark_id=loc_id)
    gallery = Gallery.objects.filter(
        landmark_id=loc_id, user_id=ui).order_by('-created_at')
    date_set = []
    for data in gallery:
        date_set.append(data.created_at.date())

    date_set = sorted(list(set(date_set)))

    result_dict = {}
    for date in date_set:
        tmp_list = []
        for i in gallery:
            if i.created_at.date() == date:
                tmp_list.append(i)
        result_dict[date] = tmp_list
    content = {
        "datas": gallery,
        "landmarks": landmark,
        'date_set': date_set,
        'result_dict': result_dict}
    return render(request, "../templates/collection/my_gallery.html", content)


def collection_ranking(request):
    rank = list(Collection.objects.values('user_id').annotate(dcount=Count('user_id')))
    rank = sorted(rank, key=lambda x: x['dcount'], reverse=True)
    rank_list = []
    if len(rank) < 10:
        idx = len(rank)
    else:
        idx = 10
    for i in range(idx):
        user = User.objects.get(id=(rank[i]['user_id']))
        tmp_dict = {}
        tmp_dict['username'] = user.nickname
        tmp_dict['cnt'] = rank[i]['dcount']
        tmp_dict['profile_photo'] = user.profile_s3_url
        tmp_dict['rank'] = (i + 1)
        tmp_dict['color'] = (i + 1) % 2
        rank_list.append(tmp_dict)

    if len(rank_list) == 1:
        rank_list.append(None)
        rank_list.append(None)

    elif len(rank_list) == 2:
        rank_list.append(None)
    return render(
        request, '../templates/collection/collection_ranking.html',
        {
            'first': rank_list[0],
            'second': rank_list[1],
            'third': rank_list[2],
            'top4_7': rank_list[3:]}
            )


def collection_update(request):
    # 카메라로 찍은 이미지 경로 설정
    path = os.getcwd()  # C:\Users\User\Desktop\potomable\git적용\Photo_Marble

    # 이미지 등록 안 하고 올릴시 새로고침
    if "camcorder" not in request.FILES:
        return redirect(".")


    # 카메라 촬영 이미지 준비
    img = request.FILES['camcorder']
    img_name = img
    img = Image.open(img)
    time = timezone.now()
    # 이미지 회전하기 90도 --> 핸드폰으로 찍으면 왼쪽으로 90회전 해서 나옴
    deg_image = img.transpose(Image.ROTATE_270)
    img = deg_image.save(path + '/collection/data/images/test.jpg')

    # yolo 실행
    conf = 0.4
    detect.run(
            conf_thres=conf,
            source=path + '/collection/data/images',
            weights=path + '/collection/best.pt',
            name=path + '/collection/detect/result',
            line_thickness=20,
            save_txt=True,
            save_conf=True,
            exist_ok=True)

    # 추론 txt파일
    directoy_list = os.listdir(path + "/collection/detect/result/labels/")
    if len(directoy_list) == 0:  # 추론 실패시
        fail_img_name = str(str(img_name)[0:5] + str(img_name)[-5:])
        img_resize(path)
        data = open(path + "/collection/detect/result/" + 'test.jpg', 'rb')
        fail_s3_url = save_s3_fail(data, fail_img_name)
        data.close()

        # 해당 결과 파일 삭제
        del_path = path + "/collection/detect/result/"
        shutil.rmtree(del_path)

        return render(
            request, '../templates/collection/collection_fail.html',
            context={"s3_url": fail_s3_url, "reason_fail": "     인식하지 못했습니다.\n      다시 촬영해주세요."})

    # 추론 txt파일 읽기 및 라벨 confidence값 불러오기
    f = open(path + "/collection/detect/result/labels/" + directoy_list[0], 'r')
    Annotate = f.readlines()[0].split()
    label = Annotate[0]
    confidence = Annotate[5]
    f.close()

    # UI에서 이미지가 너무 커서 이미지 크기 재 조정
    img_resize(path)
    # DB에 저장할 변수 지정 및 환경 설정
    user_id = request.session['id']
    landmark_id = label
    collection_info = Collection.objects.filter(user_id=user_id)
    # 랜드마크 건설할 기준 confidence
    landmark_conf = 0.3

    # 추론 성공한 이미지 s3 객체 이름
    img_name = str(str(user_id) + "_" + str(img_name)[0:5] + str(img_name)[-5:])

    # 해당 유저의 첫 업로드
    if len(collection_info) == 0:
        # 기준 confidence 값 넘으면 S3, DB에 이미지 저장 및 랜드마크 달성
        if round(float(confidence), 2) >= landmark_conf:
            # s3에 업로드 할 이미지
            data = open(path + "/collection/detect/result/" + 'test.jpg', 'rb')
            s3_url = save_s3(data, img_name)

            # DB 저장
            Collection.objects.create(
                is_visited='1',
                date=time,
                updated_at=time,
                user_id=user_id,
                landmark_id=landmark_id,
                s3_url=s3_url)
            data.close()

            # 해당 결과 파일 삭제
            del_path = path + "/collection/detect/result/"
            shutil.rmtree(del_path)

            return render(request, '../templates/collection/collection_update.html', context={"s3_url": s3_url})

        else:
            # s3에 업로드 할 이미지
            data = open(path + "/collection/detect/result/" + 'test.jpg', 'rb')
            s3_url = save_s3_fail(data=data, img_name=img_name)
            data.close()

            # 해당 결과 파일 삭제
            del_path = path + "/collection/detect/result/"
            shutil.rmtree(del_path)

            return render(
                request,
                '../templates/collection/collection_fail.html',
                context={
                    "s3_url": s3_url,
                    "reason_fail": "기준 점수를 넘지 못했습니다.\n다시 촬영해주세요"})\

    # 해당 유저의 첫 업로드 X
    else:

        # 이미 달성한 랜드마크를 촬영할 경우
        if len(Collection.objects.filter(user_id=user_id, landmark_id=landmark_id)) != 0:

            data = open(path + "/collection/detect/result/" + 'test.jpg', 'rb')
            s3_url = save_s3_fail(data=data, img_name=img_name)
            data.close()

            del_path = path + "/collection/detect/result/"
            shutil.rmtree(del_path)

            return render(
                request,
                '../templates/collection/collection_fail.html',
                context={
                    "s3_url": s3_url,
                    "reason_fail": "이미 달성한 랜드마크입니다 \a"})

        else:

            # 기준 confidence 값 넘으면 S3, DB에 이미지 저장 및 랜드마크 달성
            if round(float(confidence), 2) >= landmark_conf:

                # s3에 업로드 할 이미지
                data = open(path + "/collection/detect/result/" + 'test.jpg', 'rb')
                s3_url = save_s3(data=data, img_name=img_name)

                Collection.objects.create(
                    is_visited='1',
                    date=time,
                    updated_at=time,
                    user_id=user_id,
                    landmark_id=landmark_id,
                    s3_url=s3_url)

                data.close()

                # 해당 결과 파일 삭제
                del_path = path + "/collection/detect/result/"
                shutil.rmtree(del_path)

                return render(
                    request,
                    '../templates/collection/collection_update.html',
                    context={"s3_url": s3_url})

            else:
                # s3에 업로드 할 이미지
                data = open(path + "/collection/detect/result/" + 'test.jpg', 'rb')
                s3_url = save_s3_fail(data=data, img_name=img_name + "_under")

                # 해당 결과 파일 삭제
                del_path = path + "/collection/detect/result/"
                shutil.rmtree(del_path)

                return render(request, '../templates/collection/collection_fail.html', context={"s3_url": s3_url, "reason_fail": "기준 점수를 넘지 못했습니다.\n다시 촬영해주세요"})


def map_modal(request):
    area = Locations.objects.get(location_id=request.POST['location_id'][1:])
    landmarks = Landmark.objects.filter(area=area.name)
    land_id_lilst = [land.landmark_id for land in landmarks]
    collection = Collection.objects.filter(landmark_id__in=land_id_lilst, user_id=request.session['id'])
    coll_id_lilst = [land.landmark_id for land in collection]
    user_collection = Landmark.objects.filter(landmark_id__in=coll_id_lilst)

    return JsonResponse(
        data={
            'landmarks': list(user_collection.values())})


# ordinary functunction


def map(visited_landmark, progress):
    area_id = []
    for i in visited_landmark:
        l_d = i.landmark_id
        land = Landmark.objects.get(landmark_id=l_d)
        area_name = land.area
        land = Locations.objects.get(name=area_name)
        area_id.append('s' + str(land.location_id))

    data_list = []
    for i in range(1, 26):
        data_dict = {}
        dict_key = 's' + str(i)
        if dict_key in area_id:
            data_dict['area'] = 'area_true'
            data_dict['marker'] = 'marker'
            data_list.append(data_dict)
        else:
            data_dict['area'] = 'area_false'
            data_dict['marker'] = 'empty'
            data_list.append(data_dict)

    test_dict = {}

    for i in range(0, 25):
        test_dict['s{}'.format(i + 1)] = data_list[i]

    test_dict['progress'] = progress
    return test_dict


def my_gallery_tmp(request):
    ui = request.session['id']
    loc_id = 1
    loc = Locations.objects.get(location_id=loc_id)
    loc_name = loc.name
    lands_area = Landmark.objects.filter(area=loc_name)
    land_list = []
    for land in lands_area:
        land_list.append(land.landmark_id)
    my_galleries = Gallery.objects.filter(user=ui, landmark_id__in=land_list)

    visited_lands = []

    for my_g in my_galleries:
        visited_lands.append(my_g.landmark_id)

    landset = list(set(visited_lands))

    lands_area = Landmark.objects.filter(area=loc_name, landmark_id__in=landset)
    content = {"datas": my_galleries, "landmarks": lands_area}
    return render(request, "../templates/collection/my_gallery.html", context=content)


def collection_modal(request):
    if request.method == 'POST':
        loc_id = request.POST.get('location_list')
        if request.POST.get('my_gallery') is not None:
            return redirect('my_gallery2', loc_id)
        else:
            return redirect('photoguide2', loc_id)


def save_s3(data, img_name):
    # save results : S3로 업로드
    s3_url = "https://photomarble.s3.ap-northeast-2.amazonaws.com/yolo/success/" + img_name
    s3r = boto3.resource(
        's3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3r.Bucket('photomarble').put_object(
        Key='yolo/success/' + str(img_name), Body=data, ContentType='jpg')
    return s3_url


def save_s3_fail(data, img_name):
    # save results : S3로 업로드
    s3_url = "https://photomarble.s3.ap-northeast-2.amazonaws.com/yolo/fail/" + img_name
    s3r = boto3.resource(
        's3', aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3r.Bucket('photomarble').put_object(
        Key='yolo/fail/' + str(img_name), Body=data, ContentType='jpg')
    return s3_url


def img_resize(path):
    image = Image.open(path + "/collection/detect/result/" + 'test.jpg')
    resize_image = image.resize((256, 256))
    resize_image.save(path + "/collection/detect/result/" + 'test.jpg')
