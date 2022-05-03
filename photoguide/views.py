from django.shortcuts import render
from django.urls import reverse
from main.models import User, Collection, Landmark, Locations, Gallery
import requests
# from .DLmodel.similarity_code import FeatureExtractor
import numpy as np
import pandas as pd
from PIL import Image
import time


# Create your views here.
def photoguide(request):
    return render(request, '../templates/photoguide/photoguide.html')

def photoguide_update(request):
    img = request.FILES['file']
    features = np.load('./photoguide/DLmodel/similartiy_features.npy')

    # ---------------------------------------------api를 통한 모델 예측값 가져오기----------------------
    uploads = {'image' : request.FILES['file']}
    response = requests.post('http://127.0.0.1:8080/predict/', files = uploads)
    result = response.json()
    query = np.array(result["pred"])
    #----------------------------------------------------------------------------------------------------

    img_paths = pd.read_csv("./photoguide/DLmodel/img_paths.csv", index_col=0)
    img_paths = list(img_paths['0'])
    
    dists = np.linalg.norm(features - query, axis=1)
    ids = np.argsort(dists)
    top_url_link = [img_paths[id] for id in ids[:10]]
    # print(top_url_link)

    # print(img)
    return render(request, '../templates/photoguide/photoguide_result.html',{'imgs':top_url_link})

def photoguide_result(request):
    
    return render(request, '../templates/photoguide/photoguide_result.html')

def photoguide_result_copy(request):
    return render(request, '../templates/photoguide/photoguide_result_copy.html')