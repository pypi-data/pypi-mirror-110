class shell():
    commands = {}
    end = False
    def start():
        while True:
            worked = True
            cmd_full = input("> ").split(" ")
            cmd = cmd_full.pop(0)
            args = cmd_full
            cmd_full = None
            try:
                cmdfile = open(shell.commands[cmd], "r")
                cmdcode = cmdfile.read()
                cmdfile.close()
                if("REPLACEME" in cmdcode):
                    cmdcode = cmdcode.replace("REPLACEME", str(eval("args")))
            except Exception as error:
                print("ERROR: Command not found.")
                worked = False
            if(worked):
                try:
                    exec(cmdcode)
                except Exception as error:
                    print("ERROR: Unknown(Invalid args?)")
                    showerror = input("Display error message?[Y/n]: ")
                    if(showerror != "n"):
                        print(str(error))
            if(shell.end):
                end = False
                break
    def stop(self):
        end = True
    def add_command(command, pathtofile):
        shell.commands[command] = pathtofile
