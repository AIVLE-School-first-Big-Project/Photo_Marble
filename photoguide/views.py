from django.shortcuts import render
import requests
import numpy as np
import pandas as pd


# 포토가이드 기본페이지
def photoguide2(request, loc_id):
    return render(request, '../templates/photoguide/photoguide.html', {'loc_id': loc_id})


# 포토가이드를 위한 사진 업로드
def photoguide_update(request, loc_id):
    # 사전에 추출한 사람/배경 사진에 대한 벡터 불러오기
    persons_features = np.load('./photoguide/DLmodel/similar_persons_feature.npy')
    back_features = np.load('./photoguide/DLmodel/similar_ground_feature.npy')

    # ---------------------------------------------api를 통한 모델 예측값 가져오기----------------------
    uploads = {'image': request.FILES['file']}
    response = requests.post('http://49.164.234.56:8080/predict/', files=uploads)
    result = response.json()
    query = np.array(result["pred"])
    # ----------------------------------------------------------------------------------------------------

    # 사람과 풍경 나누기
    # persons
    person_list = []
    persons_paths = pd.read_csv("./photoguide/DLmodel/persons_paths.csv", index_col=0)

    # 쿼리와 거리를 계산
    dists = np.linalg.norm(persons_features - query, axis=1)
    ids = np.argsort(dists)
    # 계산된 값에 대한 아이디를 기준으로 s3링크와 랜드마크 아이디 저장
    for id in ids:
        df_row = persons_paths.loc[id]
        if df_row['name'] == loc_id:
            person_list.append(df_row['link'])

    # s3의 링크를 불러오기 위한 배경 csv 파일 불러오기
    background_list = []
    background_paths = pd.read_csv("./photoguide/DLmodel/background_paths.csv", index_col=0)

    # 쿼리와 거리를 계산
    dists = np.linalg.norm(back_features - query, axis=1)
    ids = np.argsort(dists)
    # 계산된 값에 대한 아이디를 기준으로 s3링크와 랜드마크 아이디 저장
    for id in ids:
        df_row = background_paths.loc[id]
        if df_row['name'] == loc_id:
            background_list.append(df_row['link'])

    return render(request, '../templates/photoguide/photoguide_result.html', {
                                                                            'persons_imgs': person_list,
                                                                            'back_imgs': background_list})


# 유사 추천 결과화면
def photoguide_result(request):
    return render(request, '../templates/photoguide/photoguide_result.html')
