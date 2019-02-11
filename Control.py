#!/usr/bin/env python

""" Control.py for creating and updating tasks """

__author__      = "gitrust"
__revision__    = "$Rev: 55 $"

import Util
from Task import Task
from colorama import init
from termcolor import colored
from colorama import  Style, Fore, Back

# colorama.init
init(autoreset=True)

class Control:
    def __init__(self):
        self.currenttask=None
        self.idgen=0
        self.tasks={}
   
    def status(self):
        """Print status information about tasks"""
        self._update()

        self._echo("")

        if self.currenttask:
            self._echo("active:\t#{} {}".format(self.currenttask.id,self.currenttask.name))
        
        # check for pause task
        self._echo("pause:\t{}h".format(Util.format_duration(self.tasks["1"].duration)))
        
        # day work time
        sum = 0
        for id in self.tasks:
            sum += self.tasks[id].duration
        
        pausetime = self._get_pause_task().duration
        # minus pause time
        sum = sum - pausetime
        self._echo("worktime:\t{}h".format(Util.format_duration(sum)))
        
        # start time of the day
        self._echo("started:\t{}".format(Util.format_starttime(self.tasks)))
        
        # presumambly end time
        self._echo("8hours:\t{}".format(Util.format_endtime(self.tasks)))

        # nr of tasks
        self._echo("tasks:\t{}".format(len(self.tasks)))

    def pause(self):
        """Create a pause task and schedule it immediately"""
        self._update()

        # create a pause task
        if len(self.tasks) == 0:
            task = Task(self.__nextid(),"pause",Util.now_sec(),Task.TYPE_PAUSE)
            self.tasks[str(task.id)] = task
            
        # set pause task to active, 
        # it is the task with the first id
        for key in self.tasks:
            t = self.tasks[key]
            if t.type == Task.TYPE_PAUSE:
                self._setcurrent(t)
 
    def commit(self,id):
        """Commit a task with specific id.
           If a task exist with this id, it will be set to done
           and a new task with the same name will be created and
           scheduled immediately.
        """
        task = self.gettask(id)
        
        # dont commit pause tasks
        # only active tasks are committed
        if task and task.type != Task.TYPE_PAUSE and task.status in (Task.STATUS_ACTIVE, Task.STATUS_INACTIVE):
            # copy task name
            name = task.name
            is_current = self._is_current(task)
            
            self.done(id)
            
            # add a new one with the same name
            self.addtask(name,is_current)
                
        
    # start an existing task
    def starttask(self,id):
        """Start a task with the given id"""
        task = self.gettask(id)
       
        # skip already running
        if task:
            if self.currenttask.id != id:
                task.status = Task.STATUS_ACTIVE
                self._setcurrent(task)
                self._echo("active task: #{}".format(id))
            else:
                self._echo("task #{} already active".format(id))
        else:
            self._echo("task #{} not found".format(id))
    
    
    def removetask(self,id):
        """Remove a task with the given id"""
        if str(id) in self.tasks:
            del self.tasks[str(id)]
        
        # also delete pointer to active task
        if self.currenttask and self.currenttask.id == id:
            self.currenttask = None
            # go to pause
            self.pause()
    
    def rename(self,id,name):
        """Rename a task with specific id"""
        task = self.gettask(id)
        if task and task.type != Task.TYPE_PAUSE and name:
            task.name = name
    
    def done(self,id):
        """Set task status to DONE and pause if no task is running"""
        
        task = self.gettask(str(id))
        # if task  not exist or is pause task
        # skip
        if not task or task.type == Task.TYPE_PAUSE:
            return
        
        self._update()
        
        task.done()
        self._echo("set task #{} to done".format(id))
            
        # also delete pointer to active task if this task was running before
        if self._is_current(task):
            self.currenttask = None
            self.pause()
            
    def gettask(self,id):
        """Returns a task for the specified task id
        
        Args:
          id (int): task id
        """
        if (str(id) in self.tasks):
            return self.tasks[str(id)]
        return None
    
    # create a new task and start it
    # add it to repository
    def addtask(self,name, set_to_current=True):
        """Add a new task with the specified task name
        
        Args:
          name (str): task name
          set_to_current (Bool): set to current task, default=True
        """
        
        # create new task
        task = Task(self.__nextid(), name, Util.now_sec())
        self.tasks[str(task.id)] = task
        if set_to_current:
            self._setcurrent(task)
        self._echo("added new task #{}".format(task.id))
        return task
   
    # adjust time (min) for a certain task 
    def adjust(self,id,time_in_min):
        """Adjust time for a certain task
        
        Args:
           id (int): task id
           time_in_min (int): time in min to adjust (negative/positive)
        """
        task = self.gettask(id)
        task.adjust_starttime(time_in_min)
        
    def clear(self):
        """Clear all tasks"""
        self.tasks = {}
                    
  
    def list(self,list_all=False):
        """Print all available tasks
        
        Args:
          list_all (boolean): list all tasks, default = False
        """
        
        self._update()

        pauseIsActive = self.currenttask and self.currenttask.type == Task.TYPE_PAUSE
        
        # table header
        self._printtableheader(("id","spend","update","created","status","title"))
        
        # print active task first
        if (self.currenttask):
                self._printtask(self.currenttask)

        for id in self.tasks:
            # ignore current task from list
            if (self.currenttask and str(id) == str(self.currenttask.id)):
                continue
            else:
                task = self.tasks[id]
                # ignore done tasks
                if not list_all and task.status == Task.STATUS_DONE:
                    continue
                self._printtask(task)


        
    def export_to_json(self,filename):
        """Export all tasks in json format to a file
        
        Args:
          filename (str): export filename
          
        Returns:
           False if export fails
        """
        self._update()
        
        try:
            file = open(filename,"w")
            file.write("{\n")
            for id in sorted(self.tasks):
                task = self.tasks[id]
                file.write(task.exp())
                file.write(",\n")
            file.write("}")
            
            file.close()
            self._echo("exported data to %s" % filename)
        except:
            return False
        return True
    
    def push(self,filename):
        """Push all done tasks to database repository and deletem them
        
        Args:
          filename (str): database repository file
        """
        exported = self.export_to_db(filename,only_done_tasks=True)
        
        # delete all done tasks
        if exported:
            done_keys = list(self.tasks)
            for id in done_keys:
                task = self.tasks[id]
                if task.status != task.STATUS_DONE:
                    continue
                del self.tasks[id]
        
        
    def export_to_db(self,filename, only_done_tasks=False):
        """Export all tasks to a database
        
        Args:
          filename (str): database filename to export tasks to
          only_done_tasks (bool): default=False, export only tasks with status DONE
          
        Returns:
          True if items were exported
        """
        
        self._update()
        
        mylist = []
        for id in sorted(self.tasks):
            task = self.tasks[id]
            
            # filter undone tasks
            if only_done_tasks and task.status != Task.STATUS_DONE:
                continue
            
            data={}
            data["id"] = task.id
            data["name"] = task.name
            data["start"] = task.start
            data["duration"] = task.duration
            data["type"] = task.type_to_str()
            data["status"] = task.status_to_str()
            data["created"] = task.created
            mylist.append(data)
        
        if len(mylist) > 0:
            Util.export_to_db(mylist,filename)
            return True
        return False
    
    def _get_pause_task(self):
        return self.tasks["1"]
        
    #
    # private functions
    #
    def _printtask(self,task,max_len=36):
        dur_sec = Util.format_duration(task.duration)
        updated = Util.format_minutes(task.updated)
        createtime = Util.format_minutes(task.created)
        status = task.status_to_str()
        current_task = self._is_current(task)
        task_id = task.id
        
        # mark current active task
        if current_task:
            task_id = "> " + str(task.id)
        self._printtable((task_id,dur_sec,updated,createtime,status,task.name[0:min(len(task.name),max_len)]))
    
    def _is_current(self,task):
        return self.currenttask.id == task.id
        
    def _printtable(self,fields):
        print(str(fields[0]).rjust(5) + str(fields[1]).rjust(7) + str(fields[2]).rjust(8) + "  " + str(fields[3]).rjust(8) + "  " + str(fields[4]) + "\t" + str(fields[5]))

    def _printtableheader(self,fields):
        print(Fore.RED + Style.BRIGHT + str(fields[0]).rjust(5) + str(fields[1]).rjust(7) + 
           str(fields[2]).rjust(8) + "  " + str(fields[3]).rjust(8) + "  " + str(fields[4]) + "\t" + str(fields[5]))

    def _echo(self,txt):
        print("  " + txt)
      
    def _setcurrent(self,task):
        self._update()
        
        # deactivate previous task
        oldTask = self.currenttask
        if oldTask and oldTask.id != task.id:
            oldTask.deactivate()
        
        # set the new task to current
        self.currenttask = task
        self.currenttask.status = Task.STATUS_ACTIVE
        
        # reset starttime
        self.currenttask.reset_start()
         
    def _update(self):
        if (self.currenttask != None):
            now = Util.now_sec()
            self.currenttask.update_duration(now)
            
    def __nextid(self):
        self.idgen = self.idgen + 1
        return self.idgen            