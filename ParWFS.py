import os
import shelve
_instances = {}
class ParWFS: 
    """ A wrapper class around the existing file system installed, managing copy-pasting files and stuff. This is mainly made for my shell ParodyWindows11.
    CREATED ON: 03/09/2024 (3rd Sep)
    BY: HeheBoi420 (on dc)
    FOR: Shell (ParodyWindows11)
    :D
    """
    def __init__(self, purpose="root"):
        self.currentCopiedFiles = [] # Absolute paths of files/folders in their original destination scheduled for copying. 
        self.currentCutFiles = []
        self.currentLoadedConfigFiles = {}
        self.TASK_IN_PROGRESS = [0, 0]
        self.RUNNING_APPS = {}
        self.RunAppsFrame = None
        _instances[purpose] = self
    def loadConfig(self, configFileName: str, configName: str):
        if not self.currentLoadedConfigFiles: self.currentLoadedConfigFiles = {}
        with shelve.open(configFileName) as cuh:
            self.currentLoadedConfigFiles[configName] = [configFileName, dict(cuh)]
    def editConfig(self, configName: str, keyToChange: str, valueToAdd):
        if not self.currentLoadedConfigFiles: self.currentLoadedConfigFiles = {}
        with shelve.open(self.currentLoadedConfigFiles[configName][0], writeback=True) as writeBack:
            writeBack[keyToChange] = valueToAdd
            writeBack.sync()
            self.currentLoadedConfigFiles[configName][1] = dict(writeBack)
        return self.currentLoadedConfigFiles[configName][1]
    def getConfig(self, configName: str):
        return self.currentLoadedConfigFiles[configName][1]
    def cutFiles(self, filesToCopy: list): self.currentCutFiles.extend(filesToCopy)
    def copyFiles(self, filesToCopy: list): self.currentCopiedFiles.extend(filesToCopy)
    def calculateProgressForPaste(self, targetPath, fileToCopy=None):
        if fileToCopy == None: fileToCopy = self.currentCopiedFiles + self.currentCutFiles
        for absFile in fileToCopy:
            if not os.path.isabs(absFile[0]): absFile[0] = os.path.join(absFile[1], absFile[0]).replace("\\", "/")
            if os.path.isdir(absFile[0]):
                if absFile[0][-1] == "/": absFile[0].replace("/", "")
                elif absFile[0][-1] == "\\": absFile[0].replace("\\", "")
                baseDir = os.path.basename(absFile[0])
                actualFullDir = os.path.join(targetPath, baseDir).replace("\\", "/")
                ls = []
                for file in os.listdir(absFile[0]):
                    ls.append([os.path.join(absFile[0], file).replace("\\", "/"), absFile[0]])
                self.calculateProgressForPaste(actualFullDir, ls)
            else: self.TASK_IN_PROGRESS[1] += 1
        return self.TASK_IN_PROGRESS
    def _pasteFiles(self, targetPath: str, fileToCopy = None, updaterFunc=lambda e: None):
        if fileToCopy == None: fileToCopy = self.currentCopiedFiles + self.currentCutFiles
        for absFile in fileToCopy:
            if not os.path.isabs(absFile[0]): absFile[0] = os.path.join(absFile[1], absFile[0]).replace("\\", "/")
            if os.path.isdir(absFile[0]):
                if absFile[0][-1] == "/": absFile[0].replace("/", "")
                elif absFile[0][-1] == "\\": absFile[0].replace("\\", "")
                baseDir = os.path.basename(absFile[0])
                actualFullDir = os.path.join(targetPath, baseDir).replace("\\", "/")
                os.mkdir(actualFullDir)
                ls = []
                for file in os.listdir(absFile[0]):
                    ls.append([os.path.join(absFile[0], file).replace("\\", "/"), absFile[0]])
                self._pasteFiles(actualFullDir, ls, updaterFunc)
            else: 
                baseName = os.path.basename(absFile[0])
                self.TASK_IN_PROGRESS[0]  += 1
                updaterFunc(self.TASK_IN_PROGRESS)
                with open(absFile[0], "rb") as reader: 
                    with open(os.path.join(targetPath, baseName).replace("\\", "/"), "wb") as writer:
                        writer.write(reader.read())
        self.TASK_IN_PROGRESS=[0, 0]
    def pasteFiles(self, targetPath: str, updaterFunc=lambda e: print("NONE")):
        self._pasteFiles(targetPath=targetPath, updaterFunc=updaterFunc)
        self.deleteFiles(fileToDelete=self.currentCutFiles)
    def deleteFiles(self, fileToDelete = None): 
        if fileToDelete == None: fileToDelete = self.currentCutFiles
        for absFile in fileToDelete:
            if not os.path.isabs(absFile[0]): absFile[0] = os.path.join(absFile[1], absFile[0]).replace("\\", "/")
            if os.path.isdir(absFile[0]):
                if absFile[0][-1] == "/": absFile[0].replace("/", "")
                elif absFile[0][-1] == "\\": absFile[0].replace("\\", "")
                ls = []
                for file in os.listdir(absFile[0]):
                    ls.append([os.path.join(absFile[0], file).replace("\\", "/"), absFile[0]])
                self.deleteFiles(ls)
                os.rmdir(absFile[0])
            else: 
                os.remove(absFile[0])
        fileToDelete = []
        self.TASK_IN_PROGRESS = [0, 0]



def testConsole():
    testingFS = ParWFS()
    print("ParWFS Testing Mode. \nCurrent Working Directory: " + os.getcwd())
    mode = input("Cut or copy? ")
    def __addToLs(ls: list):
        if (mode.lower() == "cut"): testingFS.cutFiles(ls)
        else: testingFS.copyFiles(ls)
    testCopyDir = input(f"Enter a test directory to {mode} from [ABSOLUTE PATHS ONLY]: ")
    testCopyFile = input(f"Enter a test filename to {mode} [ABSOLUTE PATHS ONLY]: ")
    __addToLs([[testCopyDir, os.path.dirname(testCopyDir)], [testCopyFile, os.path.dirname(testCopyFile)]])
    testPasteTarget = input("Enter the target directory to paste [ABSOLUTE PATHS ONLY]:  ")
    testingFS.pasteFiles(testPasteTarget)
    print("Finished task succesfully")

if __name__ == "__main__":
    testConsole()