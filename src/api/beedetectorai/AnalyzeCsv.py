import csv
import os

#csv format
#  0        1           2       3       4       5               6                   7                   8           9
#Time, X (pixels), Y (pixels), X (cm), Y (cm), angle, Distance_From_center , Total distance, Average velocity , place


def TimeStrToSeconds(timeStr):
    a1 = timeStr.split(':')
    hours = int(a1[0])
    minutes = int(a1[1])
    a2 = a1[2].split('.')
    seconds = int(a2[0])
    ms = int(a2[1])
    totalSeconds = hours*3600+minutes*60+seconds+ms/1000
    return totalSeconds


def isFinishMaze(allRows):
    justDeepInPassageway = {}
    for row in allRows[1:]:
        if float(row[6]) >= 7.5:
            justDeepInPassageway[row[9][-1:]] = 1
            if len(justDeepInPassageway) == 8:
                if ('1' in justDeepInPassageway and
                    '2' in justDeepInPassageway and
                    '3' in justDeepInPassageway and
                    '4' in justDeepInPassageway and
                    '5' in justDeepInPassageway and
                    '6' in justDeepInPassageway and
                    '7' in justDeepInPassageway and
                        '8' in justDeepInPassageway):
                    totalSeconds = TimeStrToSeconds(row[0])
                    return True, totalSeconds

    totalSeconds = TimeStrToSeconds(allRows[len(allRows)-1][0])
    return False, totalSeconds


def AnalyzeCsv(csvPath):
    allCsvRows = []

    with open(csvPath, 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        for row in csv_reader:
            if len(row) < 7 :
                return False
            allCsvRows.append(row)

    lastRow = allCsvRows[-1]

    totalDistance = float(lastRow[7])
    averageVel = float(lastRow[8])
    isSucceedMaze, timeToFinish = isFinishMaze(allCsvRows)

    rc = {
        'TotalDistance': totalDistance,
        'AverageVelocity': averageVel,
        'SucceedMaze': isSucceedMaze,
        'TimeToFinish': timeToFinish
    }

    return rc

def AverageManyCsvFiles(baseInputFolder):

    csvFilesPaths = []
    for root, dirs, files in os.walk(baseInputFolder):
        for file in files:
            if file[-3:].lower() == "csv":
                file1 = os.path.join(root,file)
                csvFilesPaths.append(file1)

    results = []
    totalDistances = []
    vel = []
    succeed = []
    time = []

    for csvFile in csvFilesPaths:
        res = AnalyzeCsv(csvFile)
        if res is not False:
            results.append(res)
            totalDistances.append(res['TotalDistance'])
            vel.append(res['AverageVelocity'])
            succeed.append(res['SucceedMaze'])
            time.append(res['TimeToFinish'])

    averageTotalDistance = sum(totalDistances)/len(totalDistances)
    averageVel = sum(vel)/len(vel)

    indicesSucceed = [i for i, x in enumerate(succeed) if x == True]


    succeedPercent = len(indicesSucceed)/len(succeed)

    totalTime = 0
    for i1, time1 in enumerate(time):
        if i1 in indicesSucceed:
            totalTime += time1

    averageTotalTime = totalTime/len(indicesSucceed)

    rc = {
        'TotalFiles': len(totalDistances),
        'AverageTotalDistance': averageTotalDistance,
        'AverageAverageVelocity': averageVel,
        'SucceedMazePercent': succeedPercent*100,
        'TimeToFinishOnSucceedAverage': averageTotalTime
    }

    return  rc


if __name__ == '__main__':
    #rc = AnalyzeCsv(r".\Data\movies\dst\csv\day1\S2810006.csv")

    rc = AverageManyCsvFiles(r'.\Data\movies\dst\csv')
    print(rc)