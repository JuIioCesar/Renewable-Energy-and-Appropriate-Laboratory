
import zipfile

def extractZipFile(zipFileName):
    archive = zipfile.ZipFile(zipFileName)
    for file in archive.namelist():
        archive.extract(file)

from os import listdir
from os.path import isfile, join

def filesInDirectory(directoryName):
    return [f for f in listdir(directoryName) if isfile(join(directoryName, f))]

import pandas

def dataframeFromFileWithPath(path):
    openFile = open(path, 'r')
    fileContent = openFile.read()
    dataframe = pandas.read_json(path_or_buf = fileContent)
    return dataframe

def timeDataFrameWith(year = '', month = '', day = '', hour = ''):
    dateString = "{}-{}-{} {}:00".format(day, month, year, hour)
    timeDataFrame = pandas.to_datetime([dateString], dayfirst=True)
    return timeDataFrame

def dataframesFromDirectory(directory):
    dataframesFromDirectory = []
    for file in filesInDirectory(directory):
        fileRelativePath = join(directory, file)
        dataframe = dataframeFromFileWithPath(fileRelativePath)
        # Prune the "valor enlace"
        dataframe = dataframe.drop('valorEnlace', 1)
        tokensInFileName = file.split('.')
        day = tokensInFileName[0]
        month = tokensInFileName[1]
        year = tokensInFileName[2]
        country = tokensInFileName[3]
        dataframe["country"] = country

        timeList = []
        for currentIndex in range(len(dataframe.index)):
            print("Hora: %s" % dataframe.hora[currentIndex])
            timeIndex = timeDataFrameWith(year = year, month = month, day = day, hour = str(dataframe.hora[currentIndex] - 1 % 24) )
            timeList.append(timeIndex)
        dataframe.index = pandas.Series(timeList)
        dataframesFromDirectory.append(dataframe)
    return dataframesFromDirectory

def allData():
    dataFileName = "datosdemanda"
    dataZipFileName = dataFileName + ".zip"
    extractZipFile(dataZipFileName)
    dataDirectoryName = dataFileName
    dataframes = dataframesFromDirectory(dataDirectoryName)
    all_data_sin = pandas.concat(dataframes)
    return all_data_sin

def main():
    print(allData())
    pandita = allData()
    pandita['hora'].plot(kind='hist', bins=50)

if __name__ == "__main__":
    main()
