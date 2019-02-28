#!/usr/bin/env python

"""timer.py, main console programm to manage timer tasks """

__author__      = "gitrust"
__version__     = "0.9.10"
__status__      = "Dev"

import sys
import datetime
import os
from control import Control

DBFILE = os.getenv("USERPROFILE") + "/timer.db"
JSONFILE = os.getenv("USERPROFILE") + "/timer.json"

class Tracker:
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
        print(" #<id>\t\tactivate an existing task by id")
        print(" add,a\t\tadd a new task and set to current")
        print(" adjust\t\tadjust time of a task")
        print(" commit,ci\tcommit a task with specific id")
        print(" done\t\tset a task to done")
        print(" export,exp\texport current task list to json")
        print(" help,h\t\tthis help")
        print(" list,l,ls\tlist tasks, to see done tasks use - list all")
        print(" pause,p\tset pause task to current")
        print(" push\t\tpush all done tasks to storage and remove them from list")
        print(" rename,ren\trename a task")
        print(" remove,rm\tremove a task")
        print(" status,st\tstatus information")
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
        export_ok = False
        
        try:        
            export_ok = self.control.export_to_json(JSONFILE)
        except:
            export_ok = False
        
        if not export_ok:
            return [1,"Could not export data"]
        return [0]
    
    def export_to_db(self):
        print("export to " + DBFILE)
        self.control.export_to_db(DBFILE)
        return [0]
    
    def push(self,cmdlist):
        self.control.push(DBFILE)
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
            elif arglen == 3:
                id = cmdlist[1]
                time_in_min = cmdlist[2]
                self.control.adjust(id,time_in_min)
            else:
                raise Exception("")
        except Exception as e:
            print (str(e))
            return [1,"Usage: adjust <id_from> [id_to] [-]<time_in_min>"]
        return [0]
        
    def pause(self, cmd):
        self.control.pause()
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
        list_all = len(cmd) > 1 and "all" in cmd
        list_yesterday = len(cmd) > 1 and "yesterday" in cmd
        
        if list_yesterday:
            self.control.list_yesterday(DBFILE)
        else:
            self.control.list(list_all)
        
        
        return [0]
        
    def beforeexit(self,cmd):
        return self.export_to_db()
        

def main():
    tracker = Tracker()
    tracker.pause([])
       
    
    while True:
        now = datetime.datetime.now().strftime('%H:%M')
        prompt = now + " > "
        
        result = tracker.exec_command(prompt)
        
        if result and result[0] != 0:
            # print error message from command
            print (str(result[1]))
        print()
        continue

if  __name__ =='__main__': main()
