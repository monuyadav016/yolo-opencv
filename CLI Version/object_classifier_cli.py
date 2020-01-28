import ODv1
import cv2
import json
import numpy as np
import argparse
from decimal import Decimal

# URL shown in the IP Webcam app
# url = 'http://192.168.43.7:8080/video'
url = ''


def setupCLI():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', help='Name of the config file in current directory')
    parser.add_argument('--names', help='Name of the files with classes in the current directory')
    parser.add_argument('--weights', help='Name of the weights file in the current directory')
    parser.add_argument('--url', help='URL if using IP webcam')
    parser.add_argument('--thres', help='Threshold for detection')
    parser.add_argument('--img', help='Path to the Image file')
    parser.add_argument('--video', help='Path to the Video file')
    parser.add_argument('--cap', action='store_true', help='Capture image')
    parser.add_argument('--record', action='store_true', help='Record Video')
    args = parser.parse_args()
    return args

args = setupCLI()
if args.url:
    url = args.url
args = setupCLI()
if args.cfg:
    ODv1.modelConf = args.cfg
if args.names:
    ODv1.classesFile = args.names
if args.weights:
    ODv1.modelWeights = args.weights
if args.thres:
    ODv1.confThreshold = Decimal(args.thres)
if args.img:
    ODv1.imgPath = args.img
if args.video:
    ODv1.videoPath = args.video


# ODv1.getObjectsFromImage(ODv1.imgPath)
# ODv1.getObjectsFromCamera(url)
# ODv1.getVideoFromCamera(url)
# ODv1.getObjectFromVideo()

# print(json.dumps(ODv1.getObjectsNames(), sort_keys=True, indent=4))
# print(ODv1.objects)

try:
    if args.url:
        if args.cap:
            ODv1.getObjectsFromCamera(url)
        elif args.record:
            ODv1.getVideoFromCamera(url)
    else:
        if args.cap:
            ODv1.getObjectsFromCamera(url)
        elif args.record:
            ODv1.getVideoFromCamera(url)
        elif args.img:
            ODv1.getObjectsFromImage(ODv1.imgPath)
        elif args.video:
            ODv1.getObjectFromVideo()
        else:
            ODv1.getObjectsFromImage(ODv1.imgPath)
except Exception as e:
    print(e)
finally:
    for i in range(3):
        print()
    print(json.dumps(ODv1.getObjectsNames(), sort_keys=True, indent=4))
    # print(ODv1.objects)

