import cv2

if __name__ == '__main__':
    vidcap = cv2.VideoCapture(r".\Data\movies\S2940002.MP4")
    success, image = vidcap.read()
    count = 0
    while success:
        cropImage = image[0:700, 440:1160, :]
        cv2.imwrite(r".\Data\images1/frame_%06d.jpg" % count, cropImage)     # save frame as JPEG file
        success, image = vidcap.read()
        print('Read a new frame: %d' % count)
        count += 1
        #if count == 20:
        #    break

