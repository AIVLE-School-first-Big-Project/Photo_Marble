from django.shortcuts import render
import requests
import numpy as np
import pandas as pd


# Create your views here.
def photoguide(request):
    return render(request, '../templates/photoguide/photoguide.html')


def photoguide2(request, loc_id):
    return render(request, '../templates/photoguide/photoguide.html', {'loc_id': loc_id})


def photoguide_update(request, loc_id):
    persons_features = np.load('./photoguide/DLmodel/similar_persons_feature.npy')
    back_features = np.load('./photoguide/DLmodel/similar_ground_feature.npy')

    # ---------------------------------------------api를 통한 모델 예측값 가져오기----------------------
    uploads = {'image': request.FILES['file']}
    response = requests.post('http://49.164.234.56:8080/predict/', files=uploads)
    result = response.json()
    query = np.array(result["pred"])
    # ----------------------------------------------------------------------------------------------------
    # persons
    person_list = []
    persons_paths = pd.read_csv("./photoguide/DLmodel/persons_paths.csv", index_col=0)

    dists = np.linalg.norm(persons_features - query, axis=1)
    ids = np.argsort(dists)

    for id in ids:
        df_row = persons_paths.loc[id]
        if df_row['name'] == loc_id:
            person_list.append(df_row['link'])

    # background
    background_list = []
    background_paths = pd.read_csv("./photoguide/DLmodel/background_paths.csv", index_col=0)
    dists = np.linalg.norm(back_features - query, axis=1)
    ids = np.argsort(dists)

    for id in ids:
        df_row = background_paths.loc[id]
        if df_row['name'] == loc_id:
            background_list.append(df_row['link'])

    return render(request, '../templates/photoguide/photoguide_result.html', {
                                                                            'persons_imgs': person_list,
                                                                            'back_imgs': background_list})


def photoguide_result(request):
    return render(request, '../templates/photoguide/photoguide_result.html')
