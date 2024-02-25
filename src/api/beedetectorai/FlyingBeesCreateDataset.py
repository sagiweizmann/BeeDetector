import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImagePath
from os import path

def convertImagesToVideo():
    try:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(r'.\Data\FlyingImages\testDiffOutVideo3.mp4', fourcc, 50, (1920, 1080))

        baseDir = r'.\Data\FlyingImages\testDiffImages3\\'
        outputGoodDir = baseDir

        for imgNumber in range(4274):
            path1 = outputGoodDir + "frame%06d.jpg" % imgNumber
            if path.exists(path1):
                frame = cv2.imread(path1)

                #if not out:
                #   height, width, channels = frame.shape

                out.write(frame)
                print("write frame: %d"%imgNumber)

    finally:
        out and out.release()
        cv2.destroyAllWindows()


def VideoToImages():
    return "Already exist, no?" # protect from running again and override files

    vidcap = cv2.VideoCapture(r".\Data\FlyingMovies\S3000006.MP4")
    success, image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite(r".\Data\FlyingImages\baseImages/frame_%06d.jpg" %
                    count, image)
        success, image = vidcap.read()
        print('Read a new frame: %d' % count)
        count += 1
        # if count == 20:
        #    break


def CreateDiffImagesFlying(imgNumber):
    baseDir = r'.\Data\FlyingImages\\'
    inputDir = baseDir + 'baseImages/'
    outputGoodDir = baseDir + 'testDiffImages3/'
    dstDirLabels = baseDir + 'labels3/'
    # outputFailDir = baseDir + 'dataSet/Fail/'
    img1 = Image.open(baseDir + 'FlyingRefImage.jpg').convert('L')
    img2Src = Image.open(inputDir + "frame_%06d.jpg" % imgNumber)
    img2 = img2Src.convert('L')

    img_arr1 = np.array(img1)
    img_arr2 = np.array(img2)

    width = img_arr1.shape[0]
    height = img_arr1.shape[1]

    imgDiffArr = img_arr1 - img_arr2

    idx1 = imgDiffArr < 30
    imgDiffArr[idx1] = 0

    idx2 = imgDiffArr > 220
    imgDiffArr[idx2] = 0

    beeMask = imgDiffArr != 0
    imgDiffArr2 = np.zeros(imgDiffArr.shape, np.uint8)

    # ## debugging:
    # imgDiffArr2[beeMask] = 255
    # Image.fromarray(np.uint8(imgDiffArr2)).show()
    # ##

    imgDiffArr2[beeMask] = 1

    kernel = np.ones((3, 3), np.uint8)
    imgDiffArr3 = cv2.morphologyEx(imgDiffArr2, cv2.MORPH_OPEN, kernel)

    cnts = cv2.findContours(imgDiffArr3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    draw = ImageDraw.Draw(img2Src)

    allImageLabels = []
    found = False
    isGood = False
    for c in cnts[0]:

        beeIndeices = c[:,0,:] #np.where(imgDiffArr3 == 1)
        xyMax = beeIndeices.max(0)
        xyMin = beeIndeices.min(0)

        x1 = xyMin[0]
        x2 = xyMax[0]
        y1 = xyMin[1]
        y2 = xyMax[1]

        xSize = x2-x1
        ySize = y2-y1


        #draw only the good rectangles
        if min(xSize,ySize) > 5 and xSize*ySize > 45: # 10 < xSize < 50 and 10 < ySize < 50:
            found = True
            minX = x1 / img2Src.width
            maxX = x2 / img2Src.width
            minY = y1 / img2Src.height
            maxY = y2 / img2Src.height

            x_center = float(minX) + ((float(maxX) - float(minX)) / 2.0)
            y_center = float(minY) + ((float(maxY) - float(minY)) / 2.0)
            width = float(maxX) - float(minX)
            height = float(maxY) - float(minY)

            newLine = '0 %f %f %f %f\n' % (x_center, y_center, width, height)
            allImageLabels.append(newLine)

            draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
            #isGood = True

    #img2Src.show()

    if found:
        imgPath = outputGoodDir + 'frame%06d.jpg' % imgNumber
        img2Src.save(imgPath)
        baseFileName = 'frame_%06d' % imgNumber

        with open(dstDirLabels + baseFileName + '.txt', 'w') as txtFile:
            for line in allImageLabels:
                txtFile.write(line)


    #with open(outputGoodDir + 'OutputsGood.csv', "a") as goodCsvFile:
    #    goodCsvFile.write(imgPath+',' + str(x1 / width) + ',' + str(y1 / height) + ',' + str(x2 / width) + ',' + str(y2 / height) + '\r\n')
    #else:
    #    imgPath = outputFailDir + 'frame%06d.jpg' % imgNumber
    #    img2Src.save(imgPath)
    #    with open(outputFailDir + 'OutputsFail.csv', "a") as failCsvFile:
    #        failCsvFile.write(imgPath+',' + str(x1 / width) + ',' + str(y1 / height) + ',' + str(x2 / width) + ',' + str(y2 / height )
    #                                                                      + "xSize="+str(xSize)+", Ysize="+str(ySize)+ '\r\n')

    #img2Src.show()

    #imgDiffArr3[x1,y1] = 2
    #imgDiffArr3[x2, y2] = 2

    #plt.imshow(imgDiffArr3);
    #plt.show()

    #imgDiff = Image.fromarray(imgDiffArr)



    #imgDiff.show()
    #imgDiff.save('C:/Users/97519/PycharmProjects/BeeDetector/Data/imageDiff.jpg')



if __name__ == '__main__':
    pass
    #VideoToImages()
    #CreateDiffImagesFlying(921)

    #for i in range(4100):
    #    CreateDiffImagesFlying(i)
    #    print('Image number : %d'%i)
    #convertImagesToVideo()









    '''
# train command:
set WANDB_MODE=offline
python train.py --img 1080 --batch 8 --epochs 250 --data "C:/Users/erez/PycharmProjects/BeeProject/Data/FlyingImages/yoloDataset/data.yaml" --weights yolov5s.pt


# detect command:
python detect.py --weights "C:/Users/erez/PycharmProjects/BeeProject/yolo/runs/train/exp21/weights/best.pt" --source "C:/Users/erez/PycharmProjects/BeeProject/Data/FlyingImages/baseImages/frame_001372.jpg" 


set WANDB_MODE=offline
'''