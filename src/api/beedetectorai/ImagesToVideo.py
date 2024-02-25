import cv2
from os import path

try:
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(r'.\Data\dataSet2\out.mp4', fourcc, 50, (720, 700))

    baseDir = r'.\Data\dataSet2\Good\\'
    outputGoodDir = baseDir

    for imgNumber in range(5550):
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