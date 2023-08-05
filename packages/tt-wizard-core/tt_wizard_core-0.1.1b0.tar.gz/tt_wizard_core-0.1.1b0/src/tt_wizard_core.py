#!/usr/bin/env python

class tt_wizard_core:
    import requests

    __LIST_PATH = "https://cdn.ravensburger.de/db/tiptoi.csv"

    __HEADER__={
            "Accept-Encoding": "gzip,deflate,sdch",
            "Accept-Language": "en-US,en;q=0.8",
            "User-Agent": "Chrome/33.0.1750.152",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive"}

    __mediaDict = {}

    __downloadPath = ""

    def __init__(self, downloadPath = ""):
        """ __init__(self, downloadPath = "")
        Contructor.

        (optional) param: String. Specifies path to storage location of gme files.
        """
        self.__downloadPath = downloadPath
        self.__mediaDict = {}
        self.__getAvailableMedia(self.__LIST_PATH)

    def __getAvailableMedia(self, path):
        """ 
        Downloads csv of available gme-files from __LIST_PATH and decodes them into a dictionary, where title name is used as key.
        """
        response = self.requests.get(path, headers=self.__HEADER__)
        lines = response.content.splitlines()
        response.close()
        self.__mediaList = []
        for line in lines:
            entries = line.decode('ISO-8859-1').split(',')
            url = entries[2]
            name = entries[3]
            if ".gme" in url:
                id = int(entries[0])
                version = int(entries[1])
                qualifiedName = (name + ".gme")
                self.__mediaDict[qualifiedName] = (qualifiedName, url, id, version)
    
    def __isDateString(self, dataBytes, position):
        """
        Checks whether >>position<< is located at the end of 8 ASCII integers (i.e. the timestamp) or not.

        return: True/False
        """
        for index in range(position, position - 8, -1):
            if (dataBytes[index] >= 58) or (dataBytes[index] < 48):
                return False
        return True

    def getAllAvailableTitles(self):
        """ 
        Return list of all titles that are available for download.

        return: [] -- List of String. List of titles (i.e. fileName + ".gme") that can be downloaded.
        """
        result = []
        for item in self.__mediaDict.keys():
            qualifiedName, url, id, version = self.__mediaDict[item] 
            result.append(qualifiedName)
        return result

    
    def searchEntry(self, searchString):
        """ 
        Search available media files for specified keyword.

        param: >>searchString<< -- String. Keyword to be searched in available titles.
        return: a.) [] -- Empty list if string is NOT found in any title.
                b.) [] -- List of all titles that include >>searchString<<
        """
        result = []
        for item in self.__mediaDict.keys():
            qualifiedName, url, id, version = self.__mediaDict[item] 
            if searchString.upper() in qualifiedName.upper():
                result.append(item)
        return result
        
    def downloadMedia(self, fileNameList, filePath=None):
        """ 
        Downloads media files into specified folder location.

        param1: [fileNames] -- List of Strings. File name of title that shall be downloaded to specified path.
        param2: >>filePath<< -- (Optional) String. Path to download location.
        return: No return value.
        """
        if filePath is None:
            path = self.__downloadPath
        else:
            path = filePath
        for title in fileNameList:
            (qualifiedName, url, id, versionRemote) = self.__mediaDict[title]
            print(f"Downloading: {qualifiedName}")
            response = self.requests.get(url, headers=self.__HEADER__)
            open((path + title), 'wb+').write(response.content)

    def checkForUpdate(self, fileName, filePath=None):
        """
        Checks whether an update for title named >>fileName<<, which is stored at location >>filePath<<, is required or not.

        param1: >>fileName<< -- String. Name of file to check its update status.
        param2: >>filePath<< -- (Optional) String. Path to storage location of gme-files.
        return: TRUE -- Update is required.
                FALSE -- Update is NOT required.
        """ 
        if filePath is None:
            path = self.__downloadPath
        else:
            path = filePath
            
        with open((path + fileName), mode='rb') as file:
            fileContent = file.read()
        # search end of timestamp
        dataString = "CopyRight"
        arData = bytes(dataString, 'utf-8')
        firstDot = fileContent.find(arData)
        endOfVersion = fileContent[firstDot:].find(0) + firstDot - 1
        if (fileContent[endOfVersion] >= 58) or (fileContent[endOfVersion] < 48):
            for index in range(endOfVersion - 1, 8, -1):
                if self.__isDateString(fileContent, index):
                    endOfVersion = index
                    break
        # extract timestamp
        versionLocal = (fileContent[endOfVersion] - 48) + \
                      ((fileContent[endOfVersion -1] - 48) * 10) + \
                      ((fileContent[endOfVersion - 2] - 48) * 100) + \
                      ((fileContent[endOfVersion - 3] - 48) * 1000) + \
                      ((fileContent[endOfVersion - 4] - 48) * 10000) + \
                      ((fileContent[endOfVersion - 5] - 48) * 100000) + \
                      ((fileContent[endOfVersion - 6] - 48) * 1000000) + \
                      ((fileContent[endOfVersion - 7] - 48) * 10000000)
        (qualifiedName, url, id, versionRemote) = self.__mediaDict[fileName]
        # Theoretically updates should only be required, when versionRemote > versionLocal
        # but we are choosing the currently hosted version to be the golden master.
        # Hence, whenever a version mismatch is detected, an update is suggested. 
        if versionRemote != versionLocal:
            print(f"Medium: {fileName} = Local Version: {versionLocal} vs. Remote Version: {versionRemote}")
            print("Type: " + str(type(fileContent)))
            return True
        else:
            return False

    def performAutoUpdate(self, filePath=None, dryRun=False):
        """ 
        Iterates through all downloaded gme-files and updates all that are outdated

        param1: >>filePath<< -- (Optional) String. Path to storage location of gme-files.
        param2: >>dryRun<< -- (Optional) Bool. 
                If >>true<<: Evaluate which files require an update only (without downloading the updates). 
                If >>False<<: Perform evaluation and OVERWRITE old files with their update (default).
        return: a.) [] -- Empty list if no titles was updated.
                b.) [] -- List of all titles that received an update.
        """
        from os import listdir
        if filePath is None:
            path = self.__downloadPath
        else:
            path = filePath

        gmeFiles = [gme for gme in listdir(path) if "gme" in gme]
        updatedFiles = []

        for title in gmeFiles:
            if self.checkForUpdate(title, path):
                if dryRun is False:
                    self.downloadMedium(title, path)
                updatedFiles.append(title)
        return updatedFiles