print("Microsoft Windows [Version 10.0.19042.1237]")
print("(c) Microsoft Corporation. All rights reserved.")
print()
usrname = "Viswas Anand"
password = "2314185"
usrask = input("What is your user name")
if usrask == usrname:
    print()
    print("What is the password")
    user_pass = input("What is your user password")
    if user_pass == password:
        print("Welcome")
        print()
        cmd = input("C:\\WINDOWS\\System32>")  # The CMD
        about = "about"  # Information about this CMD
        scan = "sfc /scannow"  # System file checker / scan now immediately
        disk = "chkdsk /f C:"  # Checks the volume on the disk C: and fully
        boot = "bootrec /fixmbr"  # Fixes the MBR partitions of your system
        boot_one = "bootrec /fixboot"  # Fixes problems with the bootloader and
        # system files that are required to boot
        boot_two = "bootrec /rebuildbcd"  # Rebuilds the fresh good bootloader
        d = "dir"  # shows the directory's contents
        c = "cd"  # changes (or comes a step back) in directory
        cc = "cd\\"  # changes to the root directory
        ccc = "cd.."  # same as shown in line 16
        disc = "diskpart"  # Helps to partition and manage volumes , drives and
        # other drive related things
        task_2 = "tasklist"  # Helps you to see all the process with their PIDs
        v = "ver"  # Helps you to find the kernel version
        mk = "mkdir"  # Helps you to make a folder
        rm = "rmdir"  # Helps you to delete a folder
        ds = "dism"  # Helps you to manages ISOs within command prompt
        ex = "exit"  # Helps you to exit the command prompt
        note = "notepad"  # Helps you to take notes quickly with one command in
        # this parody cmd
        ccl = "calc"  # Helps you to quickly calculate basic math calculations
        bootloaderedit = "bcdedit"  # Helps you to see the details of the
        # bootloader (Editing will arrive in the next preview builds)
        winver = "winver"  # Shows the kernel version and windows version
        ver = "ver"  # Shows the system version and the CLI version
        bug = "bugrpt"  # Helps you to report a bug or a glitch or give us a
        # recommendation
        if cmd == scan:
            print()
            first_m = input("beginning verification of system scan... "
                            "\n\nThis will take a while to complete")
            print()
            for i in range(0, 20):
                print("Missing file or corrupt file({0})".format(i))
            print("Windows has detected missing or corrupt dlls that are"
                  " important. we recommend you to restart.")
            cm = input("Restarting. After 10 seconds, press enter")
            if cm == bug:
                bug_bug = input(
                    "What is the bug \\ glitch \\ recommendation that "
                    "you are going to report about 'sfc /scannow'")
                print()
                print("Thank you for reporting your problems or"
                      " recommendations")
                a = input("Press any key to continue...")
        elif cmd == about:
            print("This is not a real cmd. The advantages are - It does"
                  " not execute anything ; It does not harm the "
                  "system ; It is parody\nit is not a clickbat non-"
                  "fuctional one. This CMD offers more than 15 Parody "
                  "commands.\nThis CMD can be used to see what the"
                  " command even do before you execute the real cmd"
                  " which is in C:\\Windows\\System32\\cmd.exe\nIf you "
                  "don't know what will do if we execute those 15 "
                  "commands, \nyou can test those with this CMD. You can"
                  " even create your own command.\nTo report"
                  "any bugs or possible suggestions, send an email to "
                  "'viswas.anand2009@gmail.com'. Have a great day.")
            Press_to_exit = input("Press ENTER to exit")
            if Press_to_exit == "bugrpt":
                print("What is the bug \\ glitch \\ recommendation that "
                      "you are going to report?")
                type_here = input("type the report here\n")
                print("Thank you for reporting this problem. ")
                bye = input("press enter to exit")
        elif cmd == disk:
            print()
            print()
            print("The type of the file system is NTFS")
            print()
            print("Cannot unlock current drive.")
            print()
            restart = input("chkdsk cannot run because the volume is in "
                            "use by another process .\nWould you like to"
                            " schedule this volume to be \nchecked the "
                            "next time the system restarts?[Y or N]")
            if restart == "Y":
                print()
                print("This volume is scheduled to be checked after the "
                      "system restarts.")
                comm = input("C:\\WINDOWS\\System32>")
                if comm == bug:
                    print()
                    bug_bug_rep = input("What is the bug \\ glitch \\ "
                                        "recommendation "
                                        "that you are going to report "
                                        "about 'chkdsk /f C:>>Y'")
                    print()
                    print("Thank you for reporting your problems or"
                          " recommendations")
                    a = input("Press any key to continue...")
            elif restart == "N":
                print()
                print("This volume would not be checked . ")
                cmd_prompt = input("Press any key to continue...")
                if cmd_prompt == bug:
                    print()
                    bug_rep = input("What is the bug \\ glitch \\ "
                                    "recommendation "
                                    "that you are going to report about "
                                    "'chkdsk /f C:>>N'")
                    print()
                    print("Thank you for reporting your problems or "
                          "recommendations")
                    print()
                    a = input("Press any key to continue...")
            else:
                print("Bad command or syntax\nInoperable program or "
                      "batch file. Try again")
                print()
                a = input("Press any key to continue...")
                if a == bug:
                    print()
                    bugger_collect = input("What is the bug \\ glitch"
                                           " \\ recommendation that you"
                                           " are going to report "
                                           "about 'chkdsk /f "
                                           "C:>>>Restart = {0}'".format(restart))
                    print()
                    print("Thank you for reporting your problems or "
                          "recommendation")
                    print()
                    aa = input("Press any key to continue...")
        elif cmd == boot:
            print()
            a = input()
            print("The command successfully completed")
            print()
            d = input("Press any key to continue...")
            if d == bug:
                print()
                buggy_collect = input("What is the bug \\ glitch \\ "
                                      "recommendation that you are going"
                                      " to report "
                                      "about 'bootrec /fixmbr'")
                print()
                print("Thank you for reporting your problems or "
                      "recommendations")
                print()
                aa = input("Press any key to continue...")
        elif cmd == boot_one:
            print()
            b = input()
            print("The command successfully completed")
            print()
            c = input("Press any key to continue...")
            if c == bug:
                print()
                buggy_collection = input("What is the bug \\ glitch \\ "
                                         "recommendation that you are "
                                         "going to report"
                                         "about 'bootrec /fixboot'")
                print()
                print("Thank you for reporting your problems or "
                      "recommendations ")
                print()
                aa = input("Press any key to continue....")
        elif cmd == boot_two:
            print()
            print("Scanning for all Windows installations...")
            print()
            print("Drive C:\\ Has Windows installed ")
            do_you = input("Do you want to add this Windows installation"
                           " to your list ? [Y or N]")
            if do_you == "Y":
                print("This windows installation has successfully added "
                      "to the boot list.")
                aa = input("Press any key to continue...")
                if aa == bug:
                    print()
                    buggy_collect = input("What is the bug \\ glitch \\ "
                                          "recommendation that you are "
                                          "going to report"
                                          "about 'bootrec /rebuildbcd>>>"
                                          "Restart = Y'")
                    print()
                    print("Thank you for reporting your problems or "
                          "recommendations")
                    print()
                    aaa = input("Press any key to continue...")
            elif do_you == "N":
                print("This windows installation is not added to the "
                      "boot list.")
                print()
                a = input("Press any key to continue...")
                if a == bug:
                    print()
                    buggy = input("What is the bug \\ glitch \\ "
                                  "recommendation that you are going to "
                                  "report about"
                                  "'bootrec /rebuildbcd>>Restart = N'")
                    print()
                    print("Thank you for reporting your problems or "
                          "recommendations")
                    print()
                    print("Press any key to continue...")
            else:
                print("bad command or incorrect syntax")
                print()
                a = input("Press any key to continue...")
                if a == bug:
                    print()
                    bug_collector_a = input("What is the bug \\ glitch "
                                            "\\ recommendation that you "
                                            "are going to "
                                            "report about 'bootrec /"
                                            "rebuildbcd>>>Restart = {0}"
                                            "'".format(do_you))
                    print()
                    print("Thank you for reporting your problems or "
                          "recommendation")
                    print()
                    aa = input("Press any key to continue")
        elif cmd == d:
            print("An error has occurred . Please try again")
            a = input("Press any key to continue...")
            print()
            if a == bug:
                bug_collector = input("What is the bug \\ glitch \\  "
                                      "recommendation that you are going"
                                      " to report about 'dir'")
                print()
                print("Thank you for reporting your problems or "
                      "recommendations")
                b = input("Press any key to continue...")
        elif cmd == c:
            print()
            ccoom = input("C:\\WINDOWS>")
            if ccoom == c:
                ccccoom = input("C:>")
        elif cmd == cc:
            print()
            ccom = input("C:\\>")
        elif cmd == task_2:
            print("tasklist.exe\n"
                  "cmd.exe\n"
                  "conhost.exe\n"
                  "py.exe\n"
                  "svchost.exe\n"
                  "csrss.exe\n"
                  "lsass.exe\n"
                  "winlogon.exe\n"
                  "explorer.exe\n"
                  "python.exe\n"
                  "pycharm.exe\n"
                  "realtek.exe\n"
                  "System Idle Process\n")
            cccomma = input("C:\\WINDOWS\\System32>")
        elif cmd == v:
            print("Microsoft Windows [Version 10.0.19042.1081]")
            nn = input("C:\\WINDOWS\\System32>")
        elif cmd == mk:
            fldrname = input("folder name is- ")
            print()
            print("The operation has successfully completed")
            print()
            cccoma = input("C:\\WINDOWS>")
            dd = "dir *.dir"
            if cccoma == dd:
                print(
                    "Addins\nappcompat\napppatch\nAppreadiness\nAssembly"
                    "\nbcastdvr\nBoot\nBranding\nCbsTemp\nCursors\nDebug"
                    "diagnostics\nDiagTrack\nDigitalLocker\nDownloaded "
                    "Program Files\nFONTS\nFavicon_ICON\nFirmware\n"
                    "System\nSystem32\nSysWoW64\nWinSxs\n{0}"
                    .format(fldrname))
                aa = input("C:\\WINDOWS>")
        elif cmd == rm:
            print("The operation completed successfully")
            print()
            cccooma = input("C:\\WINDOWS>")
            ddd = "dir *dir"
            print()
            if cccooma == ddd:
                print(
                    "Addins\nappcompat\napppatch\nAppreadiness\nAssembly"
                    "\nbcastdvr\nBoot\nBranding"
                    "\nCbsTemp\nCursors\nDebug"
                    "diagnostics\nDiagTrack\nDigitalLocker\nDownloaded "
                    "Program Files\nFONTS\nFavicon_ICON"
                    "\nFirmware\nSystem"
                    "\nSystem32\nSysWoW64\nWinSxs")
                ag = input("C:\\WINDOWS>")
        elif cmd == ds:
            print("Deployment Imagining and Servicing Tool\nVersion "
                  "10.0.19042.1081")
            print()
            print("On computer - LAPTOP 2UAK5KV1")
            print()
            dss = input("DISM>")
            exx = "exit"
            if dss == exx:
                print("Exiting DISM")
                cccc = input("Press any key to continue...")
                print()
                if cccc == bug:
                    bug_collection = input("What is the bug \\ glitch \\"
                                           " recommendation that you are"
                                           " going to report"
                                           "about 'DISM>'")
                    print()
                    print("Thank you for reporting your problems or "
                          "recommendations")
                    a = input("Press any key to continue")
        elif cmd == disc:
            print("Disk management and partitioning tool\nVersion "
                  "10.0.19042.1081")
            print()
            dis = input("DISKPART>")
            exi = "exit"
            if dis == exi:
                z = input("Exiting DISKPART...")
                print()
                print()
                ccm = input("Press any key to continue...")
                if ccm == bug:
                    bug_reporter = input("What is the bug \\ glitch \\ "
                                         "recommendations that you are "
                                         "going to report "
                                         "about 'DISKPART>'")
                    print()
                    print("Thank you for reporting your problems or "
                          "recommendations")
                    a = input("Press any key to continue...")
        elif cmd == ccc:
            hee = input("C:\\WINDOWS>")
            if hee == ccc:
                he = input("C:>")
        elif cmd == ex:
            print("exiting command prompt...")
        elif cmd == note:
            print()
            print("Notepad [Version 10.0.19042.1081]")
            print()
            notepad_notes = input("What are you going to write in this"
                                  "\n")
            print()
            print("The notes that you wrote are --\n{0}"
                  .format(notepad_notes))
            print()
            a = input("Press any key to continue...")
            if a == bug:
                bug_complaint = input("What is the bug \\ glitch \\"
                                      " recommendation that you are "
                                      "going to report"
                                      "about 'Notepad'")
                print()
                print("Thank you fo reporting the problems or "
                      "recommendations")
                print()
                b = input("Press any key to continue")
        elif cmd == ccl:
            print("Calculator [Version 10.0.19042.1081] \n")
            calculate_one = int(input("What is the first number in your "
                                      "calculation?"))
            sym = input("What symbol are you going to use ")
            calculate_two = int(input("What is the second number in your"
                                      " calculation?"))
            if sym == "*":
                print("{0}".format(calculate_one * calculate_two))
                a = input("Do you wish to add a third calculation?[Y or"
                          " N]")
                if a == "Y" or "y":
                    ssym = input("what is the operator?")
                    calculate_three = int(input("What is the third number"
                                                " "))
                    if ssym == "*":
                        print("{0}".format((calculate_one *
                                            calculate_two) *
                                           calculate_three))
                        aa = input("Press any key to continue...")
                        if aa == bug:
                            bug_reporting = input("Type your bug \\"
                                                  " glitch \\ "
                                                  "recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                    elif ssym == "-":
                        print("{0}".format((calculate_one *
                                            calculate_two) -
                                           calculate_three))
                        aaa = input("Press any key to continue...")
                        if aaa == bug:
                            bug_reporting = input("Type your bug \\ "
                                                  "glitch \\ "
                                                  "recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                    elif ssym == "+":
                        print("{0}".format((calculate_one *
                                            calculate_two) +
                                           calculate_three))
                        aaaa = input("Press any key to continue...")
                        if aaaa == bug:
                            bug_reporting = input("Type your bug \\ "
                                                  "glitch \\ "
                                                  "recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                    elif ssym == "/":
                        print("{0}".format((calculate_one *
                                            calculate_two) /
                                           calculate_three))
                        aaaaa = input("Press any key to continue...")
                        if aaaaa == bug:
                            bug_reporting = input("Type your bug \\ "
                                                  "glitch \\ "
                                                  "recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                    elif ssym == "//":
                        print("{0}".format((calculate_one *
                                            calculate_two) //
                                           calculate_three))
                        aaaaaa = input("Press any key to continue...")
                        if aaaaaa == bug:
                            bug_reporting = input("Type your bug \\ "
                                                  "glitch \\ "
                                                  "recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                else:
                    print("OK")
                    a = input("Press any key to continue")
                    if a == bug:
                        buggy = input("What is the bug \\ glitch \\"
                                      " recommendation that you are "
                                      "going to report")
                        print()
                        print("Thank you for reporting your problems or "
                              "recommendations")
                        aa = input("Press any key to continue...")
            elif sym == "-":
                print("{0}".format(calculate_one - calculate_two))
                bb = input("Do you wish to add a third calculation?[Y or"
                           " N] ")
                if bb == "Y":
                    ssym = input("what is the operator?")
                    calculate_three = int(input("What is the 3rd number"
                                                " "))
                    if ssym == "*":
                        print("{0}".format((calculate_one -
                                            calculate_two) *
                                           calculate_three))
                        bbb = input("Press any key to continue...")
                        if bbb == bug:
                            bug_reporting = input("Type your bug \\ "
                                                  "glitch \\ "
                                                  "recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                    elif ssym == "-":
                        print("{0}".format((calculate_one
                                            - calculate_two) -
                                           calculate_three))
                        bbbb = input("Press any key to continue...")
                        if bbbb == bug:
                            bug_reporting = input("Type your bug \\"
                                                  " glitch \\ "
                                                  "recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                    elif ssym == "+":
                        print("{0}".format((calculate_one -
                                            calculate_two) +
                                           calculate_three))
                        bbbbb = input("Press any key to continue...")
                        if bbbbb == bug:
                            bug_reporting = input("Type your bug \\ "
                                                  "glitch \\ "
                                                  "recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                    elif ssym == "/":
                        print("{0}".format((calculate_one -
                                            calculate_two) /
                                           calculate_three))
                        bbbbbb = input("Press any key to continue...")
                        if bbbbbb == bug:
                            bug_reporting = input("Type your bug \\ "
                                                  "glitch \\ "
                                                  "recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                    elif ssym == "//":
                        print("{0}".format((calculate_one -
                                            calculate_two) //
                                           calculate_three))
                        bbbbbbb = input("Press any key to continue...")
                        if bbbbbbb == bug:
                            bug_reporting = input("Type your bug \\ "
                                                  "glitch \\ "
                                                  "recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                else:
                    print("OK")
                    a = input("Press any key to continue...")
                    if a == bug:
                        buggy = input("What is the bug \\ glitch \\ "
                                      "recommendation that you are going"
                                      " to report")
                        print()
                        print("Thank you for reporting your problems or "
                              "recommendations")
                        aa = input("Press any key to continue...")
            elif sym == "+":
                print("{0}".format(calculate_one + calculate_two))
                cccc = input("Do you wish do you want to add a third "
                             "calculation[Y or N]")
                if cccc == "Y":
                    sssym = input("what is the operator?")
                    calculate_three = int(input("What is the third numbe"
                                                "r "))
                    if sssym == "*":
                        print("{0}".format((calculate_one +
                                            calculate_two) *
                                           calculate_three))
                        ccccc = input("Press any key to continue...")
                        if ccccc == bug:
                            bug_reporting = input("Type your bug \\ "
                                                  "glitch \\ "
                                                  "recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                    elif sssym == "-":
                        print("{0}".format((calculate_one +
                                            calculate_two) -
                                           calculate_three))
                        cccccc = input("Press any key to continue...")
                        if cccccc == bug:
                            bug_reporting = input("Type your bug \\ "
                                                  "glitch \\ "
                                                  "recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                    elif sssym == "+":
                        print("{0}".format((calculate_one +
                                            calculate_two) +
                                           calculate_three))
                        ccccccc = input("Press any key to continue...")
                        if ccccccc == bug:
                            bug_reporting = input("Type your bug \\ "
                                                  "glitch \\ "
                                                  "recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                    elif sssym == "/":
                        print("{0}".format((calculate_one +
                                            calculate_two) /
                                           calculate_three))
                        cccccccc = input("Press any key to continue...")
                        if cccccccc == bug:
                            bug_reporting = input("Type your bug \\ "
                                                  "glitch \\ "
                                                  "recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                    elif sssym == "//":
                        print("{0}".format((calculate_one +
                                            calculate_two) //
                                           calculate_three))
                        ccccccccc = input("Press any key to continue...")
                        if ccccccccc == bug:
                            bug_reporting = input("Type your bug \\ "
                                                  "glitch \\ "
                                                  "recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                else:
                    print("OK")
                    a = input("Press any key to continue...")
                    if a == bug:
                        buggy = input("What is the bug \\ glitch \\ "
                                      "recommendation that you are going"
                                      " to report")
                        print()
                        print("Thank you for reporting your problems or "
                              "recommendations")
                        aa = input("Press any key to continue...")
            elif sym == "/":
                print("{0}".format(calculate_one / calculate_two))
                dddd = input("Do you wish do you want to add a third "
                             "calculation[Y or N]")
                if dddd == "Y":
                    ssssym = input("what is the operator?")
                    calculate_three = int(input("What is the third "
                                                "number "))
                    if ssssym == "*":
                        print("{0}".format((calculate_one /
                                            calculate_two)
                                           * calculate_three))
                        ddddd = input("Press any key to continue...")
                        if ddddd == bug:
                            bug_reporting = input("Type your bug \\ "
                                                  "glitch \\ "
                                                  "recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                    elif ssssym == "-":
                        print("{0}".format((calculate_one /
                                            calculate_two) -
                                           calculate_three))
                        dddddd = input("Press any key to continue...")
                        if dddddd == bug:
                            bug_reporting = input("Type your bug \\ "
                                                  "glitch \\ "
                                                  "recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                    elif ssssym == "+":
                        print("{0}".format((calculate_one /
                                            calculate_two) +
                                           calculate_three))
                        ddddddd = input("Press any key to continue...")
                        if ddddddd == bug:
                            bug_reporting = input("Type your bug \\"
                                                  " glitch \\ "
                                                  "recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                    elif ssssym == "/":
                        print("{0}".format((calculate_one /
                                            calculate_two) /
                                           calculate_three))
                        dddddddd = input("Press any key to continue...")
                        if dddddddd == bug:
                            bug_reporting = input("Type your bug \\ "
                                                  "glitch \\ "
                                                  "recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                    elif ssssym == "//":
                        print("{0}".format((calculate_one /
                                            calculate_two) //
                                           calculate_three))
                        ddddddddd = input("Press any key to continue...")
                        if ddddddddd == bug:
                            bug_reporting = input("Type your bug \\"
                                                  " glitch \\ "
                                                  "recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                else:
                    print("OK")
                    a = input("Press any key to continue...")
                    if a == bug:
                        buggy = input("What is the bug \\ glitch \\"
                                      " recommendation that you are "
                                      "going to report")
                        print()
                        print("Thank you for reporting your problems or"
                              " recommendations")
                        aa = input("Press any key to continue...")
            elif sym == "//":
                print("{0}".format(calculate_one // calculate_two))
                eeee = input("Do you wish do you want to add a third"
                             " calculation[Y or N]")
                if eeee == "Y":
                    sssssym = input("what is the operator?")
                    calculate_three = int(input("What is the third "
                                                "number "))
                    if sssssym == "*":
                        print("{0}".format((calculate_one //
                                            calculate_two) *
                                           calculate_three))
                        eeeee = input("Press any key to continue...")
                        if eeeee == bug:
                            bug_reporting = input("Type your bug \\ "
                                                  "glitch \\"
                                                  " recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                    elif sssssym == "-":
                        print("{0}".format((calculate_one //
                                            calculate_two) -
                                           calculate_three))
                        eeeeee = input("Press any key to continue...")
                        if eeeeee == bug:
                            bug_reporting = input("Type your bug \\ "
                                                  "glitch \\ "
                                                  "recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                    elif sssssym == "+":
                        print("{0}".format((calculate_one //
                                            calculate_two) +
                                           calculate_three))
                        eeeeeee = input("Press any key to continue...")
                        if eeeeeee == bug:
                            bug_reporting = input("Type your bug \\"
                                                  " glitch \\ "
                                                  "recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                    elif sssssym == "/":
                        print("{0}".format((calculate_one //
                                            calculate_two) /
                                           calculate_three))
                        eeeeeeee = input("Press any key to continue...")
                        if eeeeeeee == bug:
                            bug_reporting = input("Type your bug \\"
                                                  " glitch \\ "
                                                  "recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                    elif sssssym == "//":
                        print("{0}".format((calculate_one //
                                            calculate_two) //
                                           calculate_three))
                        eeeeeeeee = input("Press any key to continue...")
                        print()
                        if eeeeeeeee == bug:
                            bug_reporting = input("Type your bug \\ "
                                                  "glitch \\ "
                                                  "recommendation here")
                            print()
                            print("Thank you for reporting your problems"
                                  " or recommendations")
                            aa = input("Press any key to continue...")
                else:
                    print("OK")
                    a = input("Press any key to continue...")
                    print()
                    if a == bug:
                        print()
                        buggy = input("What is the bug \\ glitch \\ "
                                      "recommendation that you are going"
                                      " to report")
                        print()
                        print("Thank you for reporting your problems or "
                              "recommendations")
                        aa = input("Press any key to continue...")
        elif cmd == bootloaderedit:
            print("Windows Boot Manager\n--------------------\n"
                  "identifier\t\t\t<8fes987f-8ilk-3r87-nuy2-g67m568r9802\n"
                  "device\t\t\t\tpartition = multi(0)disk(0)rdisk(0)partition(1)\n"
                  "description\t\t\tWindows Boot Manager\n"
                  "locale\t\t\t\ten-in\n"
                  "intergrityservices\tEnable\n\n"
                  "Windows Boot Loader\n-------------------\n"
                  "identifier\t\t\t<8f0873rt-09gh-23e5-e54p-pe540o8f894f>\n"
                  "device\t\t\t\tpartition = C:\\ \n"
                  "path\t\t\t\t\\Windows\\System32\\Winload.exe\n"
                  "description\t\t\tWindows 10 Home Single Lanugage\n"
                  "locale\t\t\t\ten-in\n")
            press_any_key = input("Press any key to continue...")
            if press_any_key == bug:
                print()
                debugger = input("What is the bug \\ glitch \\ recommendation that you are going to report"
                                 "about 'bcdedit'")
                print()
                print("Thank you for reporting your problems or recommendations ")
                print()
                close = input("Press any key to continue....")
            print("What is the bug \\ glitch \\ recommendation that you want to report about 'CMD'")
            print()
            bug_report = input("Please type your report here")
            print()
            print("Thank you for reporting this bug and please report this bug to the email \nthat we shown in "
                  "the disclaimer note in the above . so that we can fix it \neven if we forget to check the "
                  "software . ")
            print()
            a = input("Press any key to continue...")
        elif cmd == "winver":
            print("\nMicrosoft Windows [10.0.19043.1237]\n"
                  "Version 21H1\n"
                  "(c)Microsoft Corpration. All rights reserved\n\n"
                  "The Windows 10 Home Single Language operating system"
                  " and its user\ninterface are protected by trademark"
                  "and other pending or existing\nintellectual property"
                  "rights in the United States and \nother countries/"
                  "regions.\n\n\nThis Product is licensed under the"
                  " MICROSOFT SOFTWARE LICENSE\nTERMS to:\n\t"
                  "viswas.anand@outlook.com")
            bug_reporting_input = input("\n\n\tPress enter to exit\t\t")
            if bug_reporting_input == "bugrpt":
                bug_collect = input(
                    "What is the bug \\ glitch \\ recommendation that you want to report about 'BAD COMMAND'")
                print()
                print("Thank you for reporting your problems or recommendations ")
                print()
                a = input("Press any key to continue")
        else:
            print("'{0}' is not recognized as a operable command , batch file or program . ".format(cmd))
            print()
            cmm = input("C:\\WINDOWS\\System32>")
            if cmm == bug:
                print()
                bug_collect = input(
                    "What is the bug \\ glitch \\ recommendation that you want to report about 'BAD COMMAND'")
                print()
                print("Thank you for reporting your problems or recommendations ")
                print()
                a = input("Press any key to continue")
    else:
        print("Try again")
        aaa = input("Press the enter key to exit...")
else:
    print("Try again")
    print()
    aa = input("Press the enter key to open unprivileged cmd...")
    print()
    cmd = input("C:\\WINDOWS\\System32>")
    print()
    print("Access denied . You don't have enough permissions to access this file or program'{0}'".format(cmd))
    print()
    exit_now = input("Press ENTER to exit...")
    if exit_now == "bugrpt":
        print("   Application Error - bugrpt.exe                                    X\n"
              "\\/Cannot start application - bugrpt.exe.(0x800700BF)\n"
              "/\\The service (svchost.exe -k bugrpt.exe) failed to start")
        input("Press the enter to exit...(BUGRPT NOT AVAILABLE)")
