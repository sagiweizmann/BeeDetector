import math
import cv2
import json
import time
from os import path
import LoadModel
import torch
import sort
import numpy as np
import argparse


def timeStr1(count, fps):
    fps = 30
    h = int(count / fps / 60 / 60)
    m = int(count / fps / 60) - h * 60
    s = int(count / fps) - (m * 60 + h * 3600)
    f = 1000 * (count % fps / fps)
    str1 = "%02d:%02d:%02d.%03d" % (h, m, s, f)
    return str1
    
SIZE_TO_ADD = 300

colors = [

(0,0,0),
(255,0,0),
(128,0,0),
(255,255,0),
(128,128,0),
(0,255,0),
(0,128,0),
(0,255,255),
(0,128,128),
(0,0,255),
(0,0,128),
(255,0,255),
(128,0,128),
(255,255,255),
(192,192,192),
(128,128,128),


]

def timeStr2(seconds):
    h = int(seconds / 60 / 60)
    m = int(seconds / 60) - h * 60
    s = int(seconds) - (m * 60 + h * 3600)
    # f = 1000 * (count % fps / fps)
    str1 = "%02d:%02d:%02d" % (h, m, s)
    return str1


def AnalyzeVideoFlyingBees(model, inputFilePath, outCsvPath, outVideoPath=''):

    #if path.exists(outVideoPath):
    #    print("----------------------------------------------")
    #    print('video file %s already exists. Skipping', outVideoPath)
    #    return 'Video Already exists'

    try:
        csvFile = open(outCsvPath, 'w')
        csvFile.write(
            "Time, X (pixels), Y (pixels), ID \n")
            
        vidcapIn = cv2.VideoCapture(inputFilePath)
        fps = vidcapIn.get(cv2.CAP_PROP_FPS)


        width1 = int(vidcapIn.get(cv2.CAP_PROP_FRAME_WIDTH))
        height1 = int(vidcapIn.get(cv2.CAP_PROP_FRAME_HEIGHT))
        totalFrames = int(vidcapIn.get(cv2.CAP_PROP_FRAME_COUNT))


        success, image = vidcapIn.read()

        if outVideoPath:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            videoOut = cv2.VideoWriter(outVideoPath, fourcc, fps, (width1, height1))


        mot_tracker = sort.Sort(max_age=60, min_hits=1,iou_threshold=0.002)
        startTime = time.time()

        print("----------------------------------------------")
        print("Starting analyze video: %s" % inputFilePath)
        if outVideoPath:
            print("Out Video written to: %s" % outVideoPath)


        count = 0
        #detect bee stage
        while success:

            count += 1

            results = model(image[:, :, ::-1])
            results.pandas().xyxy[0]

            json1 = json.loads(results.pandas().xyxy[0].to_json(orient="records"))  # JSON img1 predictions

            newDetectsFromAI = []

            for detect1 in json1:
                if detect1['class'] == 0:
                    conf = detect1['confidence']
                    if conf>0.5 and detect1['xmax']-detect1['xmin']<24 and detect1['xmax']-detect1['xmin']>5.2:  # conf >= 0.5:
                        x1 = round(detect1['xmin'])
                        x2 = round(detect1['xmax'])
                        y1 = round(detect1['ymin'])
                        y2 = round(detect1['ymax'])

                        # cv2.imshow("a",cropImage)
                        # cv2.waitKey(3000)
                        if detect1['class'] == 0:
                            newDetectsFromAI.append([x1-SIZE_TO_ADD,y1-SIZE_TO_ADD,x2+SIZE_TO_ADD,y2+SIZE_TO_ADD, 0.99])

            newDetectsFromAI_np = np.empty((0, 5))
            if len(newDetectsFromAI) > 0:
                newDetectsFromAI_np = np.reshape(newDetectsFromAI, (len(newDetectsFromAI),5))

            newDetectsFromTracker = mot_tracker.update(newDetectsFromAI_np)


            for detect11 in newDetectsFromTracker:

                xCenter1 = (detect11[0]+detect11[1])/2
                yCenter1 = (detect11[2]+detect11[3])/2
                timeStr = timeStr1(count, fps)
                csvFile.write("%s, %d, %d, %d\n" % (timeStr, int(xCenter1), int(yCenter1), int(detect11[4])))

                colorId = int(detect11[4]) % len(colors)
                color = colors[colorId]

                if outVideoPath:
                    image = cv2.rectangle(image, (int(detect11[0]+SIZE_TO_ADD), int(detect11[1]+SIZE_TO_ADD)),
                                          (int(detect11[2]-SIZE_TO_ADD), int(detect11[3]-SIZE_TO_ADD)), color, 2)
                    if str(int(detect11[4])) == "1":
                        trackerTestId = "Center"
                    else:
                        trackerTestId =  "Bee ID: "+ str(int(detect11[4])-1)
                    # font
                    font = cv2.FONT_HERSHEY_DUPLEX
                    fontScale = 0.7
                    #color = color
                    thickness = 1
                    image = cv2.putText(image, trackerTestId, (int(detect11[0]+SIZE_TO_ADD), int(detect11[1]+SIZE_TO_ADD)-20), font, fontScale, color, thickness, cv2.LINE_4)

            if outVideoPath:
                videoOut.write(image)
            
            
            if count % fps == 1:
                processTime = time.time() - startTime
                remainTime = (processTime / count) * (totalFrames - count)
                percent = int(100 * (float(count) / float(totalFrames)))
                print('\r', end='')
                print("Processing...  %d/%d frames  |  %d%%  |  Elapsed time: %s  |  Remaining time: %s" %
                      (count, totalFrames, percent, timeStr2(processTime), timeStr2(remainTime)), end='')


            success, image = vidcapIn.read()
            #if count == 400:
            #   break

        processTime = time.time() - startTime
        print('\r', end='')
        print("Done.  %d/%d frames  |  100%%  | Total time: %s" % (count, totalFrames, timeStr2(processTime)))


    except Exception as e:
        print('Error: ' + str(e))
        rc = "Fail. Error: "+str(e)

    finally:
        if outVideoPath:
            videoOut and videoOut.release()
        csvFile.close()



    #return rc



if __name__ == '__main__':
    # Model

    #model = LoadModel.LoadModel()
    model = torch.hub.load('ultralytics/yolov5', 'custom',path=r'./Data/FlyingMovies/bestFlying.pt')


    #fileName = 'S3000022.MP4' #'S3000006.mp4'  #
    #inVideoPath = r'.\Data\FlyingMovies\\' + fileName   # S2810006.MP4'#S2940007.MP4'#S2940002.MP4'#S2810006.MP4'
    #outVideoPath = inVideoPath[:-4] + '_out31.mp4'
    #AnalyzeVideoFlyingBees(model, inVideoPath, outVideoPath)
    parser = argparse.ArgumentParser(description='Analyze flying bee video with default or custom parameters.')
    parser.add_argument('filename', type=str, help='Input video filename with path')
    args = parser.parse_args()
    outVideoPath = args.filename[:-4]+ '_out31.mp4'
    outCsvPath = outVideoPath + '.csv'

    AnalyzeVideoFlyingBees(model, args.filename, outCsvPath, outVideoPath)