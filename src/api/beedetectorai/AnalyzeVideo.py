import math
import cv2
import json
import time
from os import path
import LoadModel
import traceback
import argparse


def CalcDistance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))


def timeStr1(count, fps):
    fps = 50
    h = int(count / fps / 60 / 60)
    m = int(count / fps / 60) - h * 60
    s = int(count / fps) - (m * 60 + h * 3600)
    f = 1000 * (count % fps / fps)
    str1 = "%02d:%02d:%02d.%03d" % (h, m, s, f)
    return str1


def timeStr2(seconds):
    h = int(seconds / 60 / 60)
    m = int(seconds / 60) - h * 60
    s = int(seconds) - (m * 60 + h * 3600)
    # f = 1000 * (count % fps / fps)
    str1 = "%02d:%02d:%02d" % (h, m, s)
    return str1


def GetPlacefromAngle(angle):
    if 340 < angle or angle < 20:
        return 2
    if 25 < angle < 65:
        return 1
    if 70 < angle < 110:
        return 8
    if 115 < angle < 155:
        return 7
    if 160 < angle < 200:
        return 6
    if 205 < angle < 245:
        return 5
    if 250 < angle < 290:
        return 4
    if 295 < angle < 335:
        return 3
    else:
        return 0


def AnalyzeVideo(model, inputFilePath, outCsvPath, outVideoPath='', newFps=-1, minMoveDistnaceBetweenFramesPixels=3,
                 maxMoveDistanceBetweenFramesPixels=100):

    if path.exists(outCsvPath):
        print("----------------------------------------------")
        print('Csv file %s already exists. Skipping', outCsvPath)
        return 'Already exists'

    if path.exists(outVideoPath):
        print("----------------------------------------------")
        print('video file %s already exists. Skipping', outVideoPath)
        return 'Video Already exists'

    cm2Pixel = pixelsInCm = 25.323327288468995
    pixel2Cm = cmInPixel = 0.039489281507464113

    colorByClass = [(0, 0, 255), (255, 0, 255), (0, 255, 0)]

    xMazeMiddle = -1
    yMazeMiddle = -1

    rc = 'Done'

    try:
        csvFile = open(outCsvPath, 'w')
        csvFile.write(
            "Time, X (pixels), Y (pixels), X (cm), Y (cm), angle(deg), Distance_From_center (cm), Total distance (cm), Average velocity (cm/seconds), place \n")

        vidcapIn = cv2.VideoCapture(inputFilePath)
        fps = vidcapIn.get(cv2.CAP_PROP_FPS)
        skipFrames = 0
        ratio1 = 1
        if newFps == -1 or newFps > fps:
            newFps = fps
        else:
            ratio1 = float(fps)/newFps
            skipFrames = ratio1-1

        width1 = int(vidcapIn.get(cv2.CAP_PROP_FRAME_WIDTH))
        height1 = int(vidcapIn.get(cv2.CAP_PROP_FRAME_HEIGHT))
        totalFrames = int(vidcapIn.get(cv2.CAP_PROP_FRAME_COUNT))
        totalTimeStr = timeStr1(totalFrames, fps)

        width2 = width1 - 600
        height2 = height1 - 200

        success, image = vidcapIn.read()

        if outVideoPath:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            videoOut = cv2.VideoWriter(outVideoPath, fourcc, newFps, (width2, height2))

        count = 0
        totalDistancePixels = 0
        totalTimeMoveMs = 0
        lastRelX = 0
        lastRelY = 0
        msMove1Frame = 1000 / newFps

        firstDetectBee = True
        startTime = time.time()

        print("----------------------------------------------")
        print("Starting analyze video: %s" % inputFilePath)
        print("Results written to: %s" % outCsvPath)
        if outVideoPath:
            print("Out Video written to: %s" % outVideoPath)

        mazeMiddle = {}

        xCropDeltaMaze = 200
        yCropDeltaMaze = 250
        # find maze stage
        while success:
            xCropStart = 440


            cropImage = image[yCropDeltaMaze:450, xCropStart+xCropDeltaMaze:xCropStart +xCropDeltaMaze + 500, :]
            image = image[0:height2, 0:width2]
            count += 1

            results = model(cropImage[:, :, ::-1])
            results.pandas().xyxy[0]

            json1 = json.loads(results.pandas().xyxy[0].to_json(orient="records"))  # JSON img1 predictions

            rightCornerOfEdges = []

            if True:
                for detect1 in json1:
                    if detect1['class'] == 1:
                        #if xMazeMiddle == -1:
                            x1 = round(detect1['xmin'])
                            x2 = round(detect1['xmax'])
                            y1 = round(detect1['ymin'])
                            y2 = round(detect1['ymax'])
                            xMazeMiddle = x1 + (x2 - x1) / 2
                            yMazeMiddle = y1 + (y2 - y1) / 2
                            centerPoint = (round(xMazeMiddle), round(yMazeMiddle))
                            if centerPoint in mazeMiddle:
                                mazeMiddle[centerPoint] += detect1['confidence']
                            else:
                                mazeMiddle[centerPoint] = detect1['confidence']

            success, image = vidcapIn.read()
            if count == 100:
                break

        a = dict(sorted(mazeMiddle.items(), reverse=True , key=lambda item: item[1]))
        pt = next(iter(a))
        xMazeMiddle = pt[0] + xCropDeltaMaze
        yMazeMiddle = pt[1] + yCropDeltaMaze

                    #elif detect1['class'] == 2:
                    #    rightCornerOfEdges.append(round(detect1['xmax']))

                #if xMazeMiddle == -1:
                #    continue

                #rightCornerOfLeftEdge = min(rightCornerOfEdges)

                #lenHalfMazePixels = xMazeMiddle - rightCornerOfLeftEdge
                #lenHalfMazeCm = 13.1

                #cm2Pixel = pixelsInCm = lenHalfMazePixels / lenHalfMazeCm
                #pixel2Cm = cmInPixel = lenHalfMazeCm / lenHalfMazePixels

        if xMazeMiddle == -1:
            return 'Fail. cannot detect maze.'

        vidcapIn.set(cv2.CAP_PROP_POS_FRAMES, 0)
        success, image = vidcapIn.read()
        count = 0
        #detect bee stage
        while success:
            xCropStart = 440
            cropImage = image[0:700, xCropStart:xCropStart + 800, :]
            image = image[0:height2, 0:width2]
            count += 1

            results = model(cropImage[:, :, ::-1])
            results.pandas().xyxy[0]

            json1 = json.loads(results.pandas().xyxy[0].to_json(orient="records"))  # JSON img1 predictions

            rightCornerOfEdges = []

            #if xMazeMiddle == -1:
            #    for detect1 in json1:
            #        if detect1['class'] == 1:
            #            if xMazeMiddle == -1:
            #                x1 = round(detect1['xmin'])
            #                x2 = round(detect1['xmax'])
            #                y1 = round(detect1['ymin'])
            #                y2 = round(detect1['ymax'])
            #                xMazeMiddle = x1 + (x2 - x1) / 2
            #                yMazeMiddle = y1 + (y2 - y1) / 2
            #        elif detect1['class'] == 2:
            #            rightCornerOfEdges.append(round(detect1['xmax']))

            #    if xMazeMiddle == -1:
            #        continue

            #    rightCornerOfLeftEdge = min(rightCornerOfEdges)

            #    lenHalfMazePixels = xMazeMiddle - rightCornerOfLeftEdge
            #    lenHalfMazeCm = 13.1

                #cm2Pixel = pixelsInCm = lenHalfMazePixels / lenHalfMazeCm
                #pixel2Cm = cmInPixel = lenHalfMazeCm / lenHalfMazePixels

            avgVelCmSec = 0
            firstTime = True
            detectBee = False

            AllBeesDistanceFromLast = []

            # for detect1 in json1:
            #     if detect1['class'] == 0:
            #         conf = detect1['confidence']
            #         if conf >= 0.5:
            #             x1 = round(detect1['xmin'])
            #             x2 = round(detect1['xmax'])
            #             y1 = round(detect1['ymin'])
            #             y2 = round(detect1['ymax'])
            #
            #             xMiddle = x1 + (x2 - x1) / 2
            #             yMiddle = y1 + (y2 - y1) / 2
            #             xRel = xMiddle - xMazeMiddle
            #             yRel = (yMiddle - yMazeMiddle) * -1
            #             distanceFrom0 = math.sqrt(xRel * xRel + yRel * yRel)
            #
            #             if distanceFrom0 * pixel2Cm > 12.5:
            #                 continue
            #
            #             distanceFromLast = CalcDistance(xRel, yRel, lastRelX, lastRelY)
            #             AllBeesDistanceFromLast.append({"distanceFromLast1": distanceFromLast, })


            for detect1 in json1:
                # if detect1['class'] == 0:
                if True:
                    conf = detect1['confidence']
                    if conf >= 0.5:
                        x1 = round(detect1['xmin'])
                        x2 = round(detect1['xmax'])
                        y1 = round(detect1['ymin'])
                        y2 = round(detect1['ymax'])

                        # cv2.imshow("a",cropImage)
                        # cv2.waitKey(3000)
                        if detect1['class'] == 0 and firstTime:
                            if outVideoPath:
                                image = cv2.rectangle(image, (x1 + xCropStart, y1), (x2 + xCropStart, y2),
                                                      colorByClass[detect1['class']], 2)
                                image = cv2.rectangle(image, (2, 2), (390, 180), (40, 40, 40), -1)

                            timeStr = timeStr1(count, fps)
                            xMiddle = x1 + (x2 - x1) / 2
                            yMiddle = y1 + (y2 - y1) / 2
                            xRel = xMiddle - xMazeMiddle
                            yRel = (yMiddle - yMazeMiddle) * -1
                            distanceFrom0 = math.sqrt(xRel * xRel + yRel * yRel)

                            if distanceFrom0 * pixel2Cm > 12.5:
                                continue

                            distanceFromLast = CalcDistance(xRel, yRel, lastRelX, lastRelY)

                            if firstDetectBee:
                                distanceFromLast = 0

                            if distanceFromLast > maxMoveDistanceBetweenFramesPixels:
                                continue

                            if firstDetectBee or distanceFromLast < 20*ratio1:
                                if distanceFromLast > minMoveDistnaceBetweenFramesPixels:
                                    totalDistancePixels += distanceFromLast
                                    totalTimeMoveMs += msMove1Frame

                                lastRelX = xRel
                                lastRelY = yRel
                                detectBee = True
                                firstDetectBee = False
                            else:
                                continue

                            firstTime = False
                            angleRad = math.atan2(yRel, xRel)
                            angleDeg = angleRad * 180 / math.pi
                            if angleDeg < 0:
                                angleDeg += 360

                            place = 'center'
                            if distanceFrom0 > 110:
                                passageway = GetPlacefromAngle(angleDeg)
                                if passageway > 0:
                                    place = 'passageway %d' % passageway
                                else:
                                    continue
                                    #place = "Unknown"
                                    #return 'Fail. unknown place in frame %d' % count


                            avgVelCmSec = 0
                            if totalTimeMoveMs > 0:
                                avgVelCmSec = totalDistancePixels * pixel2Cm / (totalTimeMoveMs / 1000)

                            if outVideoPath:
                                #image = cv2.line(image, (int(xMazeMiddle + xCropStart), int(yMazeMiddle)),
                                #             (int(xMiddle + xCropStart), int(yMiddle)), (180, 180, 180),
                                #             thickness=1)
                                image = cv2.circle(image, (int(xMiddle + xCropStart), int(yMiddle)), 3, (0, 255, 0),
                                                   thickness=2)
                                textOnImage = ['Time: %s' % timeStr, 'X: %f' % (xRel * pixel2Cm),
                                               'Y: %f' % (yRel * pixel2Cm),
                                               'Angle (deg): %d' % int(angleDeg),
                                               'Distance from center: %f' % (distanceFrom0 * pixel2Cm),
                                               'Total Distance: %f' % (totalDistancePixels * pixel2Cm),
                                               'Average velocity (cm/sec): %f' % avgVelCmSec,
                                               'Place: %s' % place]
                                # font
                                font = cv2.FONT_HERSHEY_SIMPLEX
                                fontScale = 0.6
                                color = (0, 255, 0)
                                thickness = 1
                                y0, dy = 20, 20
                                for i, line in enumerate(textOnImage):
                                    y = y0 + i * dy
                                    image = cv2.putText(image, line, (10, y), font, fontScale, color, thickness,
                                                        cv2.LINE_4)

                            csvFile.write("%s, %d, %d, %f,%f, %d, %f, %f, %f, %s\n" % (timeStr, int(xRel), int(yRel),
                                                                                       xRel * pixel2Cm, yRel * pixel2Cm,
                                                                                       int(angleDeg),
                                                                                       distanceFrom0 * pixel2Cm,
                                                                                       totalDistancePixels * pixel2Cm,
                                                                                       avgVelCmSec, place))
                        # csvFile.write("Time, X (pixels), Y (pixels), X (cm), Y (cm), angle(deg), Distance_From_center (cm), Total distance (cm), place \n")

                        # maze middle:
                        image = cv2.circle(image, (int(xMazeMiddle + xCropStart), int(yMazeMiddle)), 10, colorByClass[1], 2)

                        if outVideoPath and detect1['class'] == 2 and detect1['confidence'] > 0.5:
                            image = cv2.rectangle(image, (x1 + xCropStart, y1), (x2 + xCropStart, y2),
                                                  colorByClass[detect1['class']], 2)

            if outVideoPath and not detectBee:
                timeStr = timeStr1(count, fps)
                textOnImage = ['Time: %s' % timeStr, 'X: Unknown', 'Y: Unknown', 'Angle (deg): Unknown',
                               'Distance from center: Unknown',
                               'Total Distance: %f' % (totalDistancePixels * pixel2Cm),
                               'Average velocity (cm/sec): %f' % avgVelCmSec,
                               'Place: Unknown']
                # font
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 0.6
                color = (0, 255, 0)
                thickness = 1
                y0, dy = 20, 20
                for i, line in enumerate(textOnImage):
                    y = y0 + i * dy
                    image = cv2.putText(image, line, (10, y), font, fontScale, color, thickness, cv2.LINE_4)
                firstDetectBee = True

            if outVideoPath:
                videoOut.write(image)

            if count % fps == 1:
                processTime = time.time() - startTime
                remainTime = (processTime / count) * (totalFrames - count)
                percent = int(100 * (float(count) / float(totalFrames)))
                print('\r', end='')
                print("Processing...  %d/%d frames  |  %d%%  |  Elapsed time: %s  |  Remaining time: %s" %
                      (count, totalFrames, percent, timeStr2(processTime), timeStr2(remainTime)), end='')

            for iSkip in range(int(skipFrames)):
                success, image = vidcapIn.read()
                count += 1


            success, image = vidcapIn.read()
            #if count == 400:
            #   break

        processTime = time.time() - startTime
        print('\r', end='')
        print("Done.  %d/%d frames  |  100%%  | Total time: %s" % (count, totalFrames, timeStr2(processTime)))


    except Exception as e:
        print('An error occurred:')
        traceback.print_exc()  # Print the full traceback
        rc = "Fail. Error: "+str(e)

    finally:
        if outVideoPath:
            videoOut and videoOut.release()

        csvFile.close()

    return rc



if __name__ == '__main__':

#     # Model
#
#     model = LoadModel.LoadModel()
#     fileName = '0224.mp4' # 'S2940002.MP4'  #S2880004.MP4
#     inVideoPath = r'./Data/movies/bugs/' + fileName  # S2810006.MP4'#S2940007.MP4'#S2940002.MP4'#S2810006.MP4'
#     outVideoPath = inVideoPath[:-4] + '_out33.mp4'
#     csvOutPath = outVideoPath + '.csv'
#     AnalyzeVideo(model, inVideoPath, csvOutPath, outVideoPath, newFps=50, minMoveDistnaceBetweenFramesPixels=3,
#                  maxMoveDistanceBetweenFramesPixels=7)
#
#     #fileName = 'S2940007.MP4'
#     #inVideoPath = r'.\Data\movies\\' + fileName  # S2810006.MP4'#S2940007.MP4'#S2940002.MP4'#S2810006.MP4'
#     #outVideoPath = inVideoPath[:-4] + '_out13.mp4'
#     #csvOutPath = outVideoPath + '.csv'
#     #AnalyzeVideo(model, inVideoPath, csvOutPath, outVideoPath)
    parser = argparse.ArgumentParser(description='Analyze video with default or custom parameters.')
    parser.add_argument('filename', type=str, help='Input video filename with path')
    parser.add_argument('--new_fps', type=int, default=50, help='New FPS value (default: 50)')
    parser.add_argument('--min_move_distance', type=int, default=3, help='Minimum move distance between frames in pixels (default: 3)')
    parser.add_argument('--max_move_distance', type=int, default=7, help='Maximum move distance between frames in pixels (default: 7)')
    args = parser.parse_args()
    outVideoPath = args.filename[:-4]+ '_out33.mp4'
    csvOutPath = outVideoPath + '.csv'
    # Model initialization
    model = LoadModel.LoadModel()

    # Analyzing video
    try:
        AnalyzeVideo(model, args.filename, csvOutPath, outVideoPath, args.new_fps, args.min_move_distance, args.max_move_distance)
    except Exception as e:
        print('Error: ' + str(e))
        rc = "Fail. Error: "+str(e)
        print(rc)
        exit(1)