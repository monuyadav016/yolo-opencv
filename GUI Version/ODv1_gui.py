import cv2
import numpy as np
from time import sleep
import speech_recognition as sr
from gtts import gTTS
import os
import json


#Variables
objects = [] #List of objects detected each frame along with probability
counter = {} #Number of Times each of an Object is detected
imgPath = "person.jpg"
videoPath = "kimetsu.mp4"
language = "en"
noConnection = False

#Write down conf, nms thresholds,inp width/height
confThreshold = 0.25
nmsThreshold = 0.40
inpWidth = 416
inpHeight = 416


#Load names of classes and turn that into a list
classesFile = "coco.names"
classes = None

with open(classesFile,'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

#Model configuration
modelConf = 'yolov3.cfg'
modelWeights = 'yolov3.weights'

#Set up the net
net = cv2.dnn.readNetFromDarknet(modelConf, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

#Process inputs
winName = 'DL OD with OpenCV'
cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
cv2.resizeWindow(winName, 1000,1000)



def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    classIDs = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            
            scores = detection [5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence > confThreshold:
                centerX = int(detection[0] * frameWidth)
                centerY = int(detection[1] * frameHeight)

                width = int(detection[2]* frameWidth)
                height = int(detection[3]*frameHeight )

                left = int(centerX - width/2)
                top = int(centerY - height/2)

                classIDs.append(classID)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    indices = cv2.dnn.NMSBoxes (boxes,confidences, confThreshold, nmsThreshold )

    indices = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        
        drawPred(frame, classIDs[i], confidences[i], left, top, left + width, top + height)
        objects.append([classes[classIDs[i]], confidences[i]])
        # print(classes[classIDs[i]])
        # print(confidences[i])


def drawPred(frame, classId, conf, left, top, right, bottom):
    # Draw a bounding box.
    cv2.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)

    label = '%.2f' % conf

    # Get the label for the class name and its confidence
    if classes:
        assert (classId < len(classes))
        label = '%s:%s' % (classes[classId], label)

    #A fancier display of the label from learnopencv.com 
    # Display the label at the top of the bounding box
    #labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    #top = max(top, labelSize[1])
    #cv2.rectangle(frame, (left, top - round(1.5 * labelSize[1])), (left + round(1.5 * labelSize[0]), top + baseLine),
                 #(255, 255, 255), cv2.FILLED)
    # cv2.rectangle(frame, (left,top),(right,bottom), (255,255,255), 1 )
    #cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)
    cv2.putText(frame, label, (left,top), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)

def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
   
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

def getVideoFromCamera(url=''):
    global noConnection
    global objects
    try:
        if not url:
            cap = cv2.VideoCapture(0)
        else:
            cap = cv2.VideoCapture(url)
        # img_counter = 0
        while True:

            #get frame from video
            hasFrame, frame = cap.read()
            if hasFrame is None:
                print('Unable to read video from webcam')

            #Create a 4D blob from a frame
            
            blob = cv2.dnn.blobFromImage(frame, 1/255, (inpWidth, inpHeight), [0,0,0], 1, crop = False)

            #Set the input the the net
            net.setInput(blob)
            outs = net.forward (getOutputsNames(net))

            postprocess (frame, outs)
            #show the image
            cv2.imshow(winName, frame)
            print(json.dumps(getObjectsNames(), sort_keys=True, indent=4))
            objects = []
            k = cv2.waitKey(1)
            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            # elif k%256 == 32:
                # SPACE pressed
                # imgPath = "opencv_frame_{}.png".format(img_counter)
                # cv2.imwrite(imgPath, frame)
                # print("{} written!".format(imgPath))
                # img_counter += 1
    except Exception as e:
        print(str(e))
        noConnection = True
    finally:
        cap.release()
        print('Exiting')
        print('Cam Released')
        cv2.destroyAllWindows()
        if noConnection:
            noConnection = False
            return False
        else:
            return True


def getObjectsFromCamera(url=''):
    global noConnection
    try:
        if not url:
            cap = cv2.VideoCapture(0)
        else:
            cap = cv2.VideoCapture(url)
        img_counter = 0
        # if not url:
        #     sleep(3)
        #get frame from video
        hasFrame, frame = cap.read()
        if hasFrame is None:
            print('Unable to read Image from camera')

        #Create a 4D blob from a frame
        
        blob = cv2.dnn.blobFromImage(frame, 1/255, (inpWidth, inpHeight), [0,0,0], 1, crop = False)
        #Set the input the the net
        net.setInput(blob)
        outs = net.forward (getOutputsNames(net))


        postprocess (frame, outs)

        # while True:
        #     #show the image
        #     cv2.imshow(winName, frame)
        #     k = cv2.waitKey(1)
        #     if k%256 == 27:
        #         # ESC pressed
        #         print("Escape hit, closing...")
        #         break

        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
    except Exception as e:
        print(str(e))
        noConnection = True
    finally:
        cap.release()
        print('Exiting')
        print('Cam Released')
        cv2.destroyAllWindows()
        if noConnection:
            noConnection = False
            return False
        else:
            return True

def getObjectsFromImage(imgPath):
    frame = cv2.imread(imgPath,cv2.IMREAD_COLOR)
    blob = cv2.dnn.blobFromImage(frame, 1/255, (inpWidth, inpHeight), [0,0,0], 1, crop = False)

    #Set the input the the net
    net.setInput(blob)
    outs = net.forward (getOutputsNames(net))


    postprocess (frame, outs)

    #show the image
    # cv2.imshow(winName, frame)
    # sleep(15)
    cv2.destroyAllWindows()

def getObjectFromVideo(videoPath):
    global objects
    try:
        cap = cv2.VideoCapture(videoPath)
        # while not cap.isOpened():
        #     cap = cv2.VideoCapture(videoPath)
        #     cv2.waitKey(1000)
        #     print("Wait for the header")

        # pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        while True:
            flag, frame = cap.read()
            if flag:
                blob = cv2.dnn.blobFromImage(frame, 1/255, (inpWidth, inpHeight), [0,0,0], 1, crop = False)

                #Set the input the the net
                net.setInput(blob)
                outs = net.forward (getOutputsNames(net))

                postprocess (frame, outs)
                if cv2.waitKey(1) > 0:
                    break
                cv2.imshow('video', frame)
                objects = []
                # print(objects)
    except Exception as e:
        print(str(e))
    finally:
        cap.release()
        print('Exiting')
        print('Cam Released')
        cv2.destroyAllWindows()

# try:
#     # Speech Recognizer Code
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Speak Now")
#         audio = recognizer.listen(source)

#     recog_text = recognizer.recognize_google(audio)
#     if "hello" in recog_text:
#         send_text = "Hello There"
#         print(send_text)
#         output = gTTS(text=send_text, lang=language, slow=False)
#         output.save("output.mp3")
#     elif "see" in recog_text:
#         print(recog_text)
#         send_text = "I can see "
#         getObjectsFromCamera()
#         for obj in objects:
#             send_text += obj[0]
#         output = gTTS(text=send_text, lang=language, slow=False)
#         output.save("see.mp3")
# except Exception as e:
#     print(str(e))
# finally:
#     cv2.destroyAllWindows()
    
def getObjectsNames():
    global counter
    counter = {}
    for object in objects:
        for detected in object:
            if detected in counter:
                counter[detected] += 1
            else:
                counter[detected] = 1
            break
    return counter

# getVideoFromCamera()
# getObjectsFromCamera()
# getObjectsFromImage(imgPath)
# getObjectFromVideo(videoPath)

# print(objects)
# print(json.dumps(getObjectsNames(), sort_keys=True, indent=4))

