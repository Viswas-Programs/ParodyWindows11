import os
import urllib3
import zipfile
from io import BytesIO
import time
print("Windows 11 v2.0 series installer...")
locationToInstall = input("Please specify the location of install. A 'root' folder will be created in that place!(If this folder, pls enter 'CURRENT') -> ")
_FOLDER = os.getcwd()
if (locationToInstall != "CURRENT"): os.mkdir(locationToInstall + "/root"); _FOLDER = locationToInstall + "/root"
else: os.mkdir(_FOLDER + "/root")
os.chdir(_FOLDER + "/root")
python3 = input("Do you want to use python3 or python in command? [Y for python3, N for python]:")
command = "python"
if (python3.lower() != "n"): command = "python3"
choice = input("Do you want to proceed with the installation or not: [Y/N]")
if choice.lower() == "n": print("Exiting installer"); os._exit(0)
print("\nStarting download of Windows 11...")
Windows11MainFile = urllib3.request("GET", "https://raw.githubusercontent.com/Viswas-Programs/ParodyWindows11/main/Windows%2011.py").data.decode("utf-8")
with open("Windows 11.py", "w") as writeOS:
    writeOS.write(Windows11MainFile)
print("Wrote the main OS File! Writing Program data (ProgramFiles)...\n")
ProgramFilesDownload = urllib3.request("GET", "https://raw.githubusercontent.com/Viswas-Programs/ParodyWindows11/main/ProgramFiles.zip").data
PrograFile = zipfile.ZipFile(BytesIO(ProgramFilesDownload))
PrograFile.extractall("ProgramFiles")
print("Finished, booting into configuration mode to finish up creating the user. ")
os.system(f"""{command} "Windows 11.py" -config """)

rebootToSystem = input("Installation FINISHED! Do you want to boot into the system now? [Y/N]")
if rebootToSystem.lower() == "n": print("Exiting installer..."); os._exit(0)
print("Thank you for installing ParodyWin11! You are going to get put into the desktop...")
time.sleep(3)
os.system(f"""{command} "Windows 11.py"  """)

