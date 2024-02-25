import os
import LoadModel
import AnalyzeVideo
from pathlib import Path
import time



def inputPathToOutputsPath(baseInputFolder, baseOutputCsvFolder, baseOutputVideoFolder, inputFilePath):
    csvOutputPath = inputFilePath.replace(baseInputFolder, baseOutputCsvFolder)
    csvOutputPath = csvOutputPath[:-4] +'.csv'

    videoOutputPath = inputFilePath.replace(baseInputFolder, baseOutputVideoFolder)

    return csvOutputPath, videoOutputPath



def AnalyzeFiles(baseInputFolder, baseOutputCsvFolder, baseOutputVideoFolder, namesFilter, newFps=5, minMoveDistnaceBetweenFramesPixels=3,
                 maxMoveDistanceBetweenFramesPixels=100):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    statusFilePath = os.path.join(baseOutputCsvFolder, 'AnalyzeFilesStatus_%s.csv' % timestr)

    allMp4InBaseInput = []
    for root, dirs, files in os.walk(baseInputFolder):
        for file in files:
            if file[-3:].lower() == "mp4":
                file1 = os.path.join(root,file)
                allMp4InBaseInput.append(file1)

    fileForProcess = []
    if len(namesFilter) > 0:
        for filter in namesFilter:
            for file1 in allMp4InBaseInput:
                if filter.lower() in file1.lower():
                    fileForProcess.append(file1)
    else:
        fileForProcess = allMp4InBaseInput


    alreadyExistsFiles = []
    runAgain = True
    while runAgain:
        runAgain = False
        for file3 in fileForProcess:
            csvOutputPath, videoOutputPath = inputPathToOutputsPath(baseInputFolder, baseOutputCsvFolder,
                                                                    baseOutputVideoFolder, file3)

            if os.path.exists(csvOutputPath) or os.path.exists(videoOutputPath):
                fileForProcess.remove(file3)
                runAgain = True
                alreadyExistsFiles.append(file3)

    try:
        csvDirPath1 = os.path.dirname(statusFilePath)
        Path(csvDirPath1).mkdir(parents=True, exist_ok=True)
        statusFile = open(statusFilePath, 'w')
        statusFile.write('File path,status,files left\n')


        numFilesToProcess = len(fileForProcess)
        for file2 in alreadyExistsFiles:
            line1 = file2 +',Already exist,%d'%numFilesToProcess
            statusFile.write(line1+'\n')
            print(line1)


        if numFilesToProcess > 0:
            model = LoadModel.LoadModel()

            for count1, file3 in enumerate(fileForProcess):
                csvOutputPath, videoOutputPath = inputPathToOutputsPath(baseInputFolder, baseOutputCsvFolder,
                                                                    baseOutputVideoFolder, file3)

                try:
                    print('=================================')
                    print('Start process file %d/%d:' % (count1+1, numFilesToProcess))
                    csvDirPath = os.path.dirname(csvOutputPath)
                    videoDirPath = os.path.dirname(videoOutputPath)
                    Path(csvDirPath).mkdir(parents=True, exist_ok=True)
                    Path(videoDirPath).mkdir(parents=True, exist_ok=True)
                    rc = AnalyzeVideo.AnalyzeVideo(model, file3, csvOutputPath, videoOutputPath, newFps,
                                                   minMoveDistnaceBetweenFramesPixels, maxMoveDistanceBetweenFramesPixels)
                except Exception as e1:
                    rc = str(e1)

                statusFile.write(file3+','+rc+',' + str(numFilesToProcess-count1)+'\n')

        print('============= Done ===============')

    finally:
        statusFile.close()



if __name__ == '__main__':
    AnalyzeFiles(r'.\Data\movies\src',
                 r'.\Data\movies\dst\csv',
                 r'.\Data\movies\dst\video',
                 [], newFps=5, minMoveDistnaceBetweenFramesPixels=3)

