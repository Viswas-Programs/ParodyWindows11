import os
import shelve
import datetime
import pickle
_instances = {}

class CallbackWrapper:
    def __init__(self, function):
        self.function = function
    def __call__(self, *args, **kwds):
        self.function(*args, **kwds)
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
        self.ROOT = None
        self.GLOBAL_VARS = None
        self.FS_STOP_RESUME_OBJECT = []
        self.STOP_CALLED = {}
        self.RESUME_CALL = {}
        self.CAME_FROM_FS_LOADS = False
        self._resetStopReumeCalls()
        _instances[purpose] = self
    def loadToPickle(self):
        temp = dict(self.STOP_CALLED)
        del temp["updaterFunc"]
        temp["TASK_IN_PROGRESS_LIST"] = self.TASK_IN_PROGRESS
        temp["COPIED_FILES"] = self.currentCopiedFiles
        temp["CUT_FILES"] = self.currentCutFiles
        try:
            with open("ProgramFiles/FS_STOP_DUMP.pkl", "wb") as DUMP: pickle.dump([temp, self.RESUME_CALL], DUMP)
        except Exception as EXP: print(EXP); return False
        else: return True
    
    def loadFromPickle(self):
        try:
            with open("ProgramFiles/FS_STOP_DUMP.pkl", "rb") as LOAD: 
                temp, self.RESUME_CALL = pickle.load(LOAD)
                for key in dict(temp).keys(): 
                    if key != "updaterFunc":  self.STOP_CALLED[key] = temp[key]
                self.TASK_IN_PROGRESS = temp["TASK_IN_PROGRESS_LIST"]
                self.CAME_FROM_FS_LOADS = True
                self.currentCopiedFiles = temp["COPIED_FILES"]
                self.currentCutFiles = temp["CUT_FILES"]
        except Exception as EXP: print(EXP); return False
        else: return True
        
    def _resetStopReumeCalls(self):
        self.STOP_CALLED = {
            "called": False,
            "reason": "",
            "time": "",
            "stoppingPath_FILE": "",
            "stoppingPath_DIR": "",
            "callFrom": "",
            "target": "",
            "updaterFunc": None,
            "stopped": False,
            "copiedFiles": None,
            "cutFiles": None
        }
        self.RESUME_CALL = {
            "called": False,
            "reason": "",
            "stoppingPath_FILE": "",
            "stoppingPath_DIR": "",
            "callFrom": "",
            "target": "",
            "time": "",
            "resumed": False
        }
        self.FS_STOP_RESUME_OBJECT = [self.STOP_CALLED, self.RESUME_CALL]
    def callStop(self, reason: str, callFrom: str):
        self.STOP_CALLED["called"] = True
        self.STOP_CALLED["reason"] = reason
        self.STOP_CALLED["callFrom"] = callFrom
        self.STOP_CALLED["time"] = datetime.datetime.now()
    def callResume(self, reason: str, callFrom: str):
        self.RESUME_CALL["called"] = True
        self.RESUME_CALL["reason"] = reason
        self.RESUME_CALL["callFrom"] = callFrom
        self.RESUME_CALL["time"] = datetime.datetime.now()
        self.pasteFiles(self.STOP_CALLED["target"], updaterFunc=self.STOP_CALLED["updaterFunc"])
    def loadConfig(self, configFileName: str, configName: str):
        if not self.currentLoadedConfigFiles: self.currentLoadedConfigFiles = {}
        try: 
            with shelve.open(configFileName) as cuh: self.currentLoadedConfigFiles[configName] = [configFileName, dict(cuh)]
            return self.currentLoadedConfigFiles[configName][1]
        except Exception as EXP: print(EXP)
    def unloadConfig(self, configName):
        try:
            del self.currentLoadedConfigFiles[configName]
        except Exception as EXP:
            print(f"Cannot unload config {configName}!\n{EXP}")
    def editConfig(self, configName: str, keyToChange: str, valueToAdd):
        if not self.currentLoadedConfigFiles: self.currentLoadedConfigFiles = {}
        with shelve.open(self.currentLoadedConfigFiles[configName][0], writeback=True) as writeBack:
            writeBack[keyToChange] = valueToAdd
            writeBack.sync()
            self.currentLoadedConfigFiles[configName][1] = dict(writeBack)
        return self.currentLoadedConfigFiles[configName][1]
    def getConfig(self, configName: str):
        try:
            return self.currentLoadedConfigFiles[configName][1]
        except Exception: return False
    def cutFiles(self, filesToCopy: list): self.currentCutFiles.extend(filesToCopy)
    def copyFiles(self, filesToCopy: list): self.currentCopiedFiles.extend(filesToCopy)
    def calculateProgressForPaste(self, targetPath, fileToCopy=None):
        self.TASK_IN_PROGRESS[1] = 0
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
    def _pasteFiles(self, targetPath: str, fileToCopy = None, updFunc=lambda e: None):
        updaterFunc = updFunc
        self.STOP_CALLED["updaterFunc"] = updaterFunc
        if self.STOP_CALLED["stopped"] == True and self.RESUME_CALL["called"] == False: return
        if fileToCopy == None: fileToCopy = self.currentCopiedFiles + self.currentCutFiles
        for absFile in fileToCopy:
            if not os.path.isabs(absFile[0]): absFile[0] = os.path.join(absFile[1], absFile[0]).replace("\\", "/")
            if os.path.isdir(absFile[0]):
                if absFile[0][-1] == "/": absFile[0].replace("/", "")
                elif absFile[0][-1] == "\\": absFile[0].replace("\\", "")
                baseDir = os.path.basename(absFile[0])
                actualFullDir = os.path.join(targetPath, baseDir).replace("\\", "/")
                try: os.mkdir(actualFullDir)
                except: pass
                ls = []
                for file in os.listdir(absFile[0]):
                    ls.append([os.path.join(absFile[0], file).replace("\\", "/"), absFile[0]])
                self._pasteFiles(actualFullDir, ls, updaterFunc)
            else: 
                baseName = os.path.basename(absFile[0])
                if self.STOP_CALLED["called"] == True and self.STOP_CALLED["stopped"] == False:
                    self.STOP_CALLED["stoppingPath_DIR"] = self.RESUME_CALL["stoppingPath_DIR"] = targetPath
                    self.STOP_CALLED["stoppingPath_FILE"] = self.RESUME_CALL["stoppingPath_FILE"] =  baseName
                    self.STOP_CALLED["stopped"] = True
                    return
                if (self.RESUME_CALL["called"] == True) and (self.RESUME_CALL["resumed"] == False):
                    if (self.RESUME_CALL["stoppingPath_FILE"] != baseName) and (absFile[1] != self.RESUME_CALL["stoppingPath_DIR"]): continue
                    else: 
                        self.RESUME_CALL["resumed"] = True
                        oldTarget = self.STOP_CALLED["target"] 
                        self._resetStopReumeCalls()
                        self.STOP_CALLED["target"] = oldTarget
                self.TASK_IN_PROGRESS[0]  += 1
                updaterFunc(self.TASK_IN_PROGRESS)
                with open(absFile[0], "rb") as reader: 
                    with open(os.path.join(targetPath, baseName).replace("\\", "/"), "wb") as writer:
                        writer.write(reader.read())
        
    def pasteFiles(self, targetPath: str, updaterFunc=lambda e: print(end="")):
        print(self.STOP_CALLED.items(), self.RESUME_CALL.items())
        self.STOP_CALLED["target"] = targetPath
        self.STOP_CALLED["updaterFunc"] = updaterFunc
        if (self.CAME_FROM_FS_LOADS and not self.RESUME_CALL["called"]): self.callResume("Resuming from a FS_STOP_DUMP", "ParWFS pasteFiles()")
        else:
            self._pasteFiles(targetPath=targetPath, updFunc=updaterFunc)
            self.TASK_IN_PROGRESS=[0, 0]
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
    def __del__(self):
        print("E")
        if self.TASK_IN_PROGRESS == [0, 0]: return False
        print("HERE!")
        self.callStop("__del__ called while performing an IO operation! Doing this for continuation in next initialization!", "ParWFS")
        while self.STOP_CALLED["stopped"] != True: pass
        else:
            self.loadToPickle()
            if not self.getConfig("SYS_CONFIG"): self.loadConfig("ProgramFiles/SYS_CONFIG", "SYS_CONFIG")
            self.editConfig("SYS_CONFIG", "FS_STOP_PREMATURE", True)
            self.unloadConfig("SYS_CONFIG")
        return True




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