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
    persons_features = np.load('./photoguide/DLmodel/similar_persons_feature.npy')
    back_features = np.load('./photoguide/DLmodel/similar_ground_feature.npy')

    # ---------------------------------------------api를 통한 모델 예측값 가져오기----------------------
    uploads = {'image' : request.FILES['file']}
    response = requests.post('http://49.164.234.56:8080/predict/', files = uploads)
    result = response.json()
    query = np.array(result["pred"])
    #----------------------------------------------------------------------------------------------------

    persons_paths = pd.read_csv("./photoguide/DLmodel/persons_paths.csv", index_col=0)
    persons_paths = list(persons_paths['0'])
    
    dists = np.linalg.norm(persons_features - query, axis=1)
    ids = np.argsort(dists)
    persons_url_link = [persons_paths[id] for id in ids[:10]]

    background_paths = pd.read_csv("./photoguide/DLmodel/background_paths.csv", index_col=0)
    background_paths = list(background_paths['0'])
    
    dists = np.linalg.norm(back_features - query, axis=1)
    ids = np.argsort(dists)
    background_url_link = [background_paths[id] for id in ids[:10]]
    
    print(persons_url_link)
    print(background_url_link)
    return render(request, '../templates/photoguide/photoguide_result.html',{
                                                                            'persons_imgs':persons_url_link,
                                                                            'back_imgs':background_url_link})

def photoguide_result(request):
    
    return render(request, '../templates/photoguide/photoguide_result.html')

def photoguide_result_copy(request):
    return render(request, '../templates/photoguide/photoguide_result_copy.html')