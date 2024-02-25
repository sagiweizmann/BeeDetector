import numpy as np
import math
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImagePath
import cv2


def CreateRefImage():
    img1 = Image.open(r".\Data\images1\frame_000116.jpg")
    img2 = Image.open(r".\Data\images1\frame_000434.jpg")

    #img1.show()
    #img2.show()

    img_arr1 = np.array(img1)
    img_arr2 = np.array(img2)

    unionImage = np.zeros(img_arr1.shape)
    unionImage[0:350, :, :] = img_arr2[0:350, :, :]
    unionImage[350:700, :, :] = img_arr1[350:700, :, :]

    unionImageImg = Image.fromarray(np.uint8(unionImage))
    #unionImageImg.convert('L').show()
    unionImageImg.save(r".\Data\RefImage2.jpg")
    X=4


if __name__ == '__main__':
    CreateRefImage()

