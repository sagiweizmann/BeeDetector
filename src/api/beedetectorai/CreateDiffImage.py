import numpy as np
import math
import  matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImagePath
import cv2


def CreateRefImage():
    img1 = Image.open("C:/Users/97519/PycharmProjects/BeeDetector/Data/frames3/frame_003478.jpg")
    img2 = Image.open("C:/Users/97519/PycharmProjects/BeeDetector/Data/frames3/frame_002401.jpg")

    img_arr1 = np.array(img1)
    img_arr2 = np.array(img2)

    unionImage = np.zeros(img_arr1.shape)
    unionImage[0:350, :, :] = img_arr2[0:350, :, :]
    unionImage[350:700, :, :] = img_arr1[350:700, :, :]

    unionImageImg = Image.fromarray(np.uint8(unionImage))
    #unionImageImg.show()
    unionImageImg.save('C:/Users/97519/PycharmProjects/BeeDetector/Data/RefImage.jpg')
    X=4



def DiffImage(imgNumber):
    baseDir = r'.\Data/'
    inputDir = baseDir + 'images1/'
    outputGoodDir = baseDir + 'dataSet2/Good1/'
    outputFailDir = baseDir + 'dataSet2/Fail1/'
    img1 = Image.open(baseDir + 'RefImage.jpg').convert('L')
    img2Src = Image.open(inputDir + "frame_%06d.jpg" % imgNumber)
    img2 = img2Src.convert('L')

    mazeCenter = [362, 319, 383, 341]  # x1,y1,x2,y2
    mazeEdges = [[32, 333,  39, 352],
                 [706, 310, 713, 328],
                 [378, 659, 397, 665],
                 [116, 94, 134, 110],
                 [592, 80, 607, 96],
                 [608, 549, 626, 566],
                 [138, 568, 156, 584]]

    img_arr1 = np.array(img1)
    img_arr2 = np.array(img2)

    width = img_arr1.shape[0]
    height = img_arr1.shape[1]

    #plt.imshow(img_arr2)
    #plt.show()
    imgDiffArr = img_arr1 - img_arr2

    #Image.fromarray(np.uint8(imgDiffArr)).show()

    idx1 = imgDiffArr < 30
    imgDiffArr[idx1] = 0

    idx2 = imgDiffArr > 220
    imgDiffArr[idx2] = 0

    beeMask = imgDiffArr != 0
    imgDiffArr2 = np.zeros(imgDiffArr.shape, np.uint8)
    imgDiffArr2[beeMask] = 1


    kernel = np.ones((5, 5), np.uint8)
    imgDiffArr3 = cv2.morphologyEx(imgDiffArr2, cv2.MORPH_OPEN, kernel)


    beeIndeices = np.where(imgDiffArr3 == 1)

    x1 = np.min(beeIndeices[0])
    x2 = np.max(beeIndeices[0])
    y1 = np.min(beeIndeices[1])
    y2 = np.max(beeIndeices[1])

    xSize = x2-x1
    ySize = y2-y1

    draw = ImageDraw.Draw(img2Src)
    draw.rectangle([y1, x1, y2, x2], outline="red", width=2)

    # draw maze:
    draw.rectangle(mazeCenter, outline="purple", width=3)
    for mazeEdge in mazeEdges:
        draw.rectangle(mazeEdge, outline="green", width=3)

    if 10 < xSize < 50 and 10 < ySize < 50:
        imgPath = outputGoodDir + 'frame%06d.jpg' % imgNumber
        img2Src.save(imgPath)
        with open(outputGoodDir + 'OutputsGood.csv', "a") as goodCsvFile:
            goodCsvFile.write(imgPath+',' + str(x1 / width) + ',' + str(y1 / height) + ',' + str(x2 / width) + ',' + str(y2 / height)+'\n')
    else:
        imgPath = outputFailDir + 'frame%06d.jpg' % imgNumber
        img2Src.save(imgPath)
        with open(outputFailDir + 'OutputsFail.csv', "a") as failCsvFile:
            failCsvFile.write(imgPath+',' + str(x1 / width) + ',' + str(y1 / height) + ',' + str(x2 / width) + ',' + str(y2 / height )
                                                                                      + "xSize="+str(xSize)+", Ysize="+str(ySize)+'\n')


    #img2Src.show()

    #imgDiffArr3[x1,y1] = 2
    #imgDiffArr3[x2, y2] = 2

    #plt.imshow(imgDiffArr3);
    #plt.show()

    #imgDiff = Image.fromarray(imgDiffArr)



    #imgDiff.show()
    #imgDiff.save('C:/Users/97519/PycharmProjects/BeeDetector/Data/imageDiff.jpg')


if __name__ == '__main__':
    #CreateRefImage()
    #DiffImage(2894)
    for i in range(5550):
        DiffImage(i)
        print('Image number : %d'%i)

