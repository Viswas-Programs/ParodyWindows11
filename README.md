# ParodyWindows11
A parody of an operating system. the name I chose is Windows 11
Look for more in the wiki of my project in (https://github.com/Viswas-Programs/ParodyWindows11/wiki) there.

Easy setup (if github servers work): For linux only, run dos2unix command on the Bash script, and then run the file in linux terminal, in the directory you want to install, and run the file.

Manual Setup:

Step 1: Clone the github repository using `git clone https://github.com/Viswas-Programs/ParodyWindows11`


Step 2: Switch to the desired branch (For most cases, dev branch should be stable enough), do `git checkout <branch-name>` 


Step 3: 

You can either setup a new user account but with limited configuration options with the new OOBE system (I'll update this when I include those settings in the OOBE too)

In that case, run `python3 "Windows 11.py"`

OR

Run the file with the -config parameter to create a new user account with some more choice (Just themes for now)

Run `python3 "Windows 11.py" -config` for that

You can then change these settings, some of them through the Settings app in GUI, Or by running the -configchange parameter when starting the file (`python3 "Windows 11.py" -configchange`) and selecting the appropriate selections.


SOME KNOWN BUGS: 
In Linux, keyboard inputs to text boxes and shortcut keys to DWM-Managed windows are broken and inconsistent. This is a bug that I don't know of a way to fix. It's due to Linux not giving text-bindings to rootoverrideredirect'ed windows so easily without a focus_force which breaks multi-tasking functionalities. (In Windows you don't need to worry about it, it works just fine there.)

Some distros might outright block input to the DWM-Managed window, while some other distros like Linux Mint allow input but in a whacky manner. When you move the mouse randomly through the screen (To mess with the focus of widgets) then hover over your desired window and textbox and then start typing, it should work. This is really inconsistent behaviour. 

Will try to fix it but I don't think it's easy since it's a problem that's with the way Linux manages windows that isn't under it's own window manager's control

Have a great time playing around!
