from django.shortcuts import render
from . import ODv1
import cv2
import json
import os
import numpy as np
import argparse
from decimal import Decimal

# Create your views here.
def home(request):
    # URL shown in the IP Webcam app
    # url = 'http://192.168.43.7:8080/video'
    url = ''

    # ODv1.getObjectsFromImage(ODv1.imgPath)
    ODv1.getObjectsFromCamera(url)
    # ODv1.getVideoFromCamera(url)
    # ODv1.getObjectFromVideo()

    objs = ODv1.getObjectsNames()
    # print(json.dumps(objs, sort_keys=True, indent=4))
    # print(ODv1.objects)
    objs = ODv1.getObjectsNames()
    context = { 'objs': objs }
    return render(request, 'website/home.html', context)
