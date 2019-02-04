#!/usr/bin/env python

"""timer.py, main console programm to manage timer tasks """

__author__      = "gitrust"
__copyright__   = "Copyright 2014"
__version__     = "0.9.6"
__revision__    = "$Rev: 55 $"
__status__      = "Dev"

import sys
import datetime
import os
from Control import Control

class Timer:
    def __init__(self):
        self.control = Control()
        print("time tracker V" + __version__)

    def exec_command(self,prompt):
        # builtin weiche zwischen verschiedenen python versionen
        if 'raw_input' in dir(__builtins__):
            rawcmd =  raw_input(prompt)
        else:
            rawcmd =  input(prompt)
        
        # command tokens
        cmdlist = self.parsecommand(rawcmd)
        
        status=[0]
        
        cmd = cmdlist[0]
        
        # execute a command
        if cmd in ("add","a"):
            status = self.addtask(cmdlist)
        elif cmd in ("list","l","ls"):
            status = self.list(cmdlist)
        elif cmd.startswith("#"):
            status = self.task(cmdlist)           
        elif cmd in ("help","h"):
            status = self.printhelp(cmdlist)
        elif cmd in ("status","st"):
            status = self.status(cmdlist)
        elif cmd in ("remove","rm"):
            status = self.removetask(cmdlist)
        elif cmd in ("exit","quit","q"):
            status = self.beforeexit(cmdlist)
            exit(0)
        elif cmd in ("exp","export"):
            status = self.export(cmdlist)
        elif cmd == "clear":
            status = self.clear(cmdlist)
        elif cmd == "done":
            status = self.done(cmdlist)
        elif cmd == "push":
            status = self.push(cmdlist)
        elif cmd in ("pause","p"):
            status = self.pause(cmdlist)
        elif cmd in ("commit","ci"):
            status = self.commit(cmdlist)
        elif cmd in ("rename","ren"):
            status = self.rename(cmdlist)
        elif cmd in ("adjust"):
            status = self.adjust(cmdlist)
        elif cmd == "":
            status = [0,""]
        else:
            status = [1,"unknown command" + str(cmdlist)]
                    
        # return [status, errortext]
        return status
    
    def printhelp(self,cmd):
        print("Available commands: ")
        print(" #<id>\t\tactivate an existing task using its id")
        print(" add,a\t\tadd a new task and activate it")
        print(" adjust\t\ttrasnfer time of one task to another or adjust time of a task")
        print(" clear,cl\tclear all tasks")
        print(" commit,ci\tcommit a task with specific id")
        print(" done\t\tset task to done")
        print(" export,exp\texport current data")
        print(" help,h\t\tthis help")
        print(" list,l,ls\tlist all available tasks")
        print(" pause,p\tpause tasks")
        print(" push\t\tpush all done tasks to repository db and remove them from current list")
        print(" rename,ren\trename a task")
        print(" remove,rm\tremove task")
        print(" status,st\tstatus about current task")
        return [0] 
    
    def parsecommand(self,commandtext):
        args =  commandtext.strip().split(" ")
        if not args:
            return [""]
        else:
            return args

    def removetask(self,cmd):        
        try:
            id = int(cmd[1])
            self.control.removetask(id)
        except:
            return [1,"remove <id>"]
        return [0]
    
    def rename(self,cmd):
        try:
            id = int(cmd[1])
            name = ' '.join(str(x) for x in cmd[2:]).strip()
            self.control.rename(id,name)
        except:
            return [1,"rename <id> <name>"]
        return [0]
        
    def done(self,cmd):
        try:
            id = int(cmd[1])
            self.control.done(id)
        except:
            return [1,"done <id>"]
        return [0]

    def addtask(self,cmd):
        try:            
            self.control.addtask(" ".join(cmd[1:]))
        except:
            return [1,"add <taskname> "]
        return [0]

    def commit(self,cmd):
        try:
            id = int(cmd[1])
            self.control.commit(id)
        except:
            return [1,"commit <id> "]
        return [0]
        
    def export(self,cmd):
        now = datetime.datetime.now()
        filename = os.getenv("USERPROFILE") + "/timer.json"
        export_ok = False
        
        try:        
            export_ok = self.control.export_to_json(filename)
        except:
            export_ok = False
        
        if not export_ok:
            return [1,"Could not export data"]
        return [0]
    
    def export_to_db(self):
        filename = os.getenv("USERPROFILE") + "/timer.db"
        print("export to " + filename)
        self.control.export_to_db(filename)
        return [0]
    
    def push(self,cmdlist):
        filename = os.getenv("USERPROFILE") + "/timer.db"
        self.control.push(filename)
        return [0]

    def adjust(self,cmdlist):

        try:
            arglen = len(cmdlist)
            # move time from one task to another
            if arglen > 3:
                id_from = cmdlist[1]
                id_to = cmdlist[2]
                time_in_min = abs(int(cmdlist[3]))
                self.control.adjust(id_from,time_in_min)
                self.control.adjust(id_from,time_in_min*-1)
            # adjust time for one task
            else:
                id = cmdlist[1]
                time_in_min = cmdlist[2]
                self.control.adjust(id,time_in_min)
        except Exception as e:
            print (str(e))
            return [1,"Usage: adjust <id_from> [id_to] [-]<time_in_min>"]
        return [0]
        
    def pause(self, cmd):
        self.control.pause()
        return [0]

    def clear(self,cmd):
        self.control.clear()
        return [0]

    def status(self,cmd):
        self.control.status()
        return [0]
        
    def task(self,cmd):
        try:
            taskid = int("".join(cmd)[1:])
            self.control.starttask(taskid)
        except:
            return [1,"#<id>"]
        return [0]        
     
    def list(self,cmd):
        list_all = len(cmd) > 1 and cmd[1] == "all"
        self.control.list(list_all)
        
        # todo description for command syntax
        return [0]
        
    def beforeexit(self,cmd):
        return self.export_to_db()
        

def main():
    timer = Timer()
    timer.pause([])
       
    
    while True:
        now = datetime.datetime.now().strftime('%H:%M')
        prompt = now + " > "
        
        result = timer.exec_command(prompt)
        
        if result[0] != 0:
            # print error message from command
            print (str(result[1]))
        continue

if  __name__ =='__main__': main()
