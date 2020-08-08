import subprocess
import os


class lexicalDic:
    KS_DIC_FOLDER = "KS-DICT"
    N_DIC_FOLDER = "N-DICT"

    LEX_DIC = "LEX-DIC\\base.dic"
    LEX_PROB_DIC = "LEX-DIC\\lpf.lst"
    RELATIVE_PATH = "\\DicMaTool_Web\\managementPython\\EXE\\"

    def makeLexicalDB(self):
        resultDict = {"result": "", "error": 0}

        fileName = "makeTransDicDB.exe"
        location = os.getcwd()
        os.chdir(self.RELATIVE_PATH)
        result = subprocess.run([self.RELATIVE_PATH + fileName], capture_output=True)
        output = result.stdout.decode('utf-8')
        os.chdir(location)

        if "DB open error!" in output:
            resultDict['result'] = "Make Lexical DB Error"
            resultDict['error'] = 1
            return resultDict

        resultDict['result'] = "Lexical Dictionary DB is created !"
        return resultDict


    def makeProbDB(self):
        resultDict = {"result": "", "error": 0}

        fileName = "makeLexProbDicDB.exe"
        location = os.getcwd()
        os.chdir(self.RELATIVE_PATH)
        result = subprocess.run([self.RELATIVE_PATH + fileName], capture_output=True)
        output = result.stdout.decode('utf-8')
        os.chdir(location)

        if "DB open error!" in output:
            resultDict['result'] = "Make Prob DB Error"
            resultDict['error'] = 1
            return resultDict

        resultDict['result'] = "Lexical Prob Dictionary DB is created !"
        return resultDict


    def lexFileSearch(self, data):
        resultDict = {"result": "", "error": 0, "message": "", "file": None}
        # generic is none  pos is domain, else pos is generic

        if not os.path.isfile(self.RELATIVE_PATH + self.LEX_DIC):
            resultDict['error'] = 1
            resultDict["message"] = self.LEX_DIC + " doesn't exist !!!"
            return resultDict
        resultDict['file'] = open(self.RELATIVE_PATH + self.LEX_DIC)
        return resultDict


    def lexSearch(self, data):
        resultDict = self.lexFileSearch(data)
        resultDict.update({"foundLine": 0})

        if resultDict['error'] == 1:
            return resultDict

        word = data['word']

        if len(word) == 0:
            resultDict['error'] = 1
            resultDict["message"] = "No Word Specified !!!"
            return resultDict

        allLines = resultDict['file'].readlines()
        keywordAllLines = [items.split(',')[0] for items in allLines] # keyword extraction

        if word in keywordAllLines :
            resultDict['foundLine'] = keywordAllLines.index(word)
            resultDict['result'] = allLines[resultDict['foundLine']]
        else :
            resultDict["error"] = 1
            resultDict["message"] = word + " is not in dictionary"
            return resultDict

        return resultDict


    def probFileSearch(self):
        resultDict = {"result": "", "error": 0, "message": "", "file": None}
        # generic is none  pos is domain, else pos is generic

        if not os.path.isfile(self.RELATIVE_PATH + self.LEX_PROB_DIC):
            resultDict['error'] = 1
            resultDict["message"] = self.LEX_PROB_DIC + " doesn't exist !!!"
            return resultDict
        resultDict['file'] = open(self.RELATIVE_PATH + self.LEX_PROB_DIC)
        return resultDict


    def probSearch(self, data):
        resultDict = self.probFileSearch()
        resultDict.update({"foundLine": 0})

        if resultDict['error'] == 1:
            return resultDict

        word = data['word']

        if len(word) == 0:
            resultDict['error'] = 1
            resultDict["message"] = "No Word Specified !!!"
            return resultDict

        allLines = resultDict['file'].readlines()
        keywordAllLines = [items.split(' ')[0] for items in allLines]  # keyword extraction

        if word in keywordAllLines:
            resultDict['foundLine'] = keywordAllLines.index(word)
            resultDict['result'] = allLines[resultDict['foundLine']]
        else:
            resultDict["error"] = 1
            resultDict["message"] = word + " is not in dictionary"
            return resultDict

        return resultDict


    def lexUpdate(self, data):
        print("lex Search")

    def probUpdate(self, data):
        print("lex Search")

    def openDicFile(self, data):
        resultDict = {"result": "", "error": 0, "message": "", "file": None}
        word = data['word']
        generic = data['generics']
        domain = data['domains'][0:3]  # POS = 3 characters
        errorMSG = ""
        POS = ""
        # generic is none  pos is domain, else pos is generic

        if len(word) == 0:
            resultDict['error'] = 1
            resultDict["message"] += "No Word Specified !!!"
            return resultDict

        if len(generic) == 0:
            POS = domain
        else:
            POS = generic

        if len(POS) == 0:
            resultDict['error'] = 1
            resultDict["message"] += "No POS specified !!!"
            return resultDict

        newDomainPOS = ""
        # general DIC: nn, vb, ...
        # domain DIC: sPos == sNewPos

        if POS not in self.CONVERT_POS:
            newDomainPOS = POS
        else:
            newDomainPOS = self.CONVERT_POS[POS]

        firstLetter = word[0].lower()

        # make dictionary file name in KS DIC folder
        folderName = ""
        if POS not in self.FOLDER_Name:
            folderName = "General"
        else:
            folderName = self.FOLDER_Name[POS]

        KSDicFullFileName = self.KS_DIC_FOLDER + "\\" + folderName + "\\"
        NDicFullFileName = self.N_DIC_FOLDER + "\\" + folderName + "\\"
        fileName = "dic"
        if newDomainPOS not in ['pron', 'prep', 'conj']:
            fileName += firstLetter
        fileName += '.'
        fileName += newDomainPOS

        NDicFullFileName += fileName

        KSDicFullFileName += fileName
        KSDicFullFileName += '.txt'

        relativePath = "\\DicMaTool_Web\\managementPython\\EXE\\"
        # when KS Dic file doesn't exist, generate file from N Dic file
        if not os.path.isfile(relativePath + KSDicFullFileName):
            self.generateKSDicFile(folderName, fileName)
            errorMSG = folderName + "\\" + fileName + " is generated !!!\n"
            resultDict["message"] = errorMSG
            # Print file generated massageBox

        if not os.path.isfile(relativePath + KSDicFullFileName):
            # print(KSDicFullFileName + " doesn't exist")
            errorMSG = KSDicFullFileName + " doesn't exist"
            resultDict['error'] = 1
            resultDict["message"] += errorMSG
            return resultDict
            # process end
        resultDict['file'] = open(relativePath + KSDicFullFileName)
        return resultDict

    def Search(self, data):
        word = data['word']

        key = "\"" + word + "\""

        resultDict = self.openDicFile(data)
        resultDict.update({"foundLine": 0, "nextEntryLine": 0})
        if resultDict['error'] == 1:
            return resultDict
        # print(allReadLines)

        allLines = resultDict['file'].readlines()
        index = 0
        # Is key in the list?
        if key + "\n" in allLines:
            index = allLines.index(key + "\n")
        else:
            # print(word + " is not in dictionary")
            errorMSG = word + " is not in dictionary"
            resultDict["error"] = 1
            resultDict["message"] = errorMSG
            return resultDict
        resultDict['foundLine'] = index

        # get key's means
        resultDict['result'] = allLines[index]

        length = 0
        for reads in allLines[index + 1:]:
            if (reads[0] == '"'):
                break
            else:
                resultDict['result'] += reads
                length += 1
        resultDict['nextEntryLine'] = length + 1

        return resultDict

    def Update(self, replaceData):
        searchResult = self.Search(replaceData)
        searchResult.update({"result": "", "errors": ""})

        # file offset reset
        searchResult['file'].seek(0)
        allLines = searchResult['file'].readlines()
        updateData = []

        # 수정 전의 부분
        updateData += allLines[: searchResult['foundLine'] - 1]
        # 수정 부분
        for item in replaceData['updateText'].split("\n"):
            updateData.append(item + "\n")  # split 과정중 사라진 \n을 붙여줌
        # 수정 이후 부분
        updateData += allLines[searchResult['foundLine'] + searchResult['nextEntryLine']:]

        domain = replaceData['domains']
        generic = replaceData['generics']
        word = replaceData['word']

        if len(generic) == 0:
            POS = domain
        else:
            POS = generic
        newDomainPOS = ""
        if POS not in self.CONVERT_POS:
            newDomainPOS = POS
        else:
            newDomainPOS = self.CONVERT_POS[POS]
        firstLetter = word[0].lower()
        # make dictionary file name in KS DIC folder
        folderName = ""
        if POS not in self.FOLDER_Name:
            folderName = "General"
        else:
            folderName = self.FOLDER_Name[POS]

        KSDicFullFileName = self.KS_DIC_FOLDER + "\\" + folderName + "\\"
        NDicFullFileName = self.N_DIC_FOLDER + "\\" + folderName + "\\"
        fileName = "dic"
        if newDomainPOS not in ['pron', 'prep', 'conj']:
            fileName += firstLetter
        fileName += '.'
        fileName += newDomainPOS

        NDicFullFileName += fileName

        KSDicFullFileName += fileName
        KSDicFullFileName += '.txt'

        relativePath = "\\DicMaTool_Web\\managementPython\\EXE\\"

        txtFileName = "KS-DICT2\\" + folderName + "\\" + fileName + ".txt"
        txtFile = open(relativePath + txtFileName, 'w')
        txtFile.write("".join(updateData))

        tmpFileName = 'tmp\\' + fileName + '.jh'

        # ksExe = "EXE\\kscode.exe"
        ksExe = "kscode.exe"
        # ksArgument = "-jk " + fileName + ".jh" + self.KS_DIC_FOLDER + "\\" + folderName + "\\" + fileName + '.txt'
        # process run kscode.exe (argument is ksArgument)
        subprocess.run([relativePath + ksExe, "-kj", relativePath + txtFileName,
                        relativePath + tmpFileName])

        # cnExe = "EXE\\cn.exe"
        cnExe = "cn.exe"
        # cnArgument = "-nc " + alterFullFileName +  " " + fileName + ".jh"
        # process run cn.exe (argument is cnArgument)
        subprocess.run([relativePath + cnExe, "-cn", relativePath + tmpFileName,
                        relativePath + "N-DICT\\" + folderName + "\\" + fileName])

        # sTxtFileName + " is created" + Environment.NewLine + "N-DICT\\" + sFolderName + "\\" + sFileName + " is created")
        replaceData[
            'result'] = txtFileName + " is created\n" + "N-DICT\\" + folderName + "\\" + fileName + " is created"

        return replaceData

    def generateKSDicFile(self, folderName, fileName):
        alterFullFileName = self.N_DIC_FOLDER + "\\" + folderName + "\\" + fileName
        relativePath = "\\DicMaTool_Web\\managementPython\\EXE\\"
        # cnExe = "EXE\\cn.exe"
        cnExe = "cn.exe"
        # cnArgument = "-nc " + alterFullFileName +  " " + fileName + ".jh"
        # process run cn.exe (argument is cnArgument)
        subprocess.run([relativePath + cnExe, "-nc", relativePath + alterFullFileName, relativePath + fileName + ".jh"])

        # ksExe = "EXE\\kscode.exe"
        ksExe = "kscode.exe"
        # ksArgument = "-jk " + fileName + ".jh" + self.KS_DIC_FOLDER + "\\" + folderName + "\\" + fileName + '.txt'
        # process run kscode.exe (argument is ksArgument)
        subprocess.run([relativePath + ksExe, "-jk", relativePath + fileName + ".jh",
                        relativePath + self.KS_DIC_FOLDER + "\\" + folderName + "\\" + fileName + '.txt'])

        # FILE delete fileName+".jh"
        removeFileName = relativePath + fileName + ".jh"
        if os.path.isfile(removeFileName):
            os.remove(removeFileName)


if __name__ == "__main__":
    testClass = lexicalDic()
    # testClass.makeGenericDB()
    testData = {'word': 'test'}
    print(testClass.probSearch(testData))
