#!/usr/bin/env python

"""Task.py - structure for Timer tasks """

__author__      = "gitrust"
__revision__    = "$Rev: 54 $"

import Util

class Task:
    # type
    TYPE_NORMAL, TYPE_PAUSE = range(2)
    # status
    STATUS_DONE, STATUS_ACTIVE, STATUS_INACTIVE = range(3)
    
    def __init__(self, id, name, start,type=TYPE_NORMAL):
        """
        Args:
          id (int):             task id
          name (str):           task name
          start (int):          task starttime, seconds since 1970
          type (NORMAL*,PAUSE): type of the task
        """
        self.id = id
        self.name = name
        self.start = start
        self.updated = start
        # in seconds
        self.duration = 0
        self.type = type
        self.status = Task.STATUS_ACTIVE
        self.created = start
    
    def touch(self):
        """Rest last access time for this task """
        self.start = Util.now_sec()
        self.updated = self.start
     
    def update_duration(self,now):
        """Update task duration using current timestamp """
        self.duration =  self.duration + (now - self.start)
        # reset to new start
        self.start = now
        self.updated = now
    
    def deactivate(self):
        self.status = Task.STATUS_INACTIVE
     
    def done(self):
        """Set status of this task to STATUS_DONE """
        self.status = Task.STATUS_DONE
        self.updated = Util.now_sec()
    
    def type_to_str(self):
        if self.type == Task.TYPE_NORMAL:
            return "NORMAL"
        elif self.type == Task.TYPE_PAUSE:
            return "PAUSE"
        return "UNKNOWN"
        
    def status_to_str(self):
        if self.status == Task.STATUS_DONE:
            return "DONE"
        elif self.status == Task.STATUS_ACTIVE:
            return "ON"
        elif self.status == Task.STATUS_INACTIVE:
            return "OFF"
        return "UNKNOWN"

    def reset_start(self):
        self.start = Util.now_sec()
        
    def adjust_starttime(self,timeinmin):
        self.duration = self.duration + (int(timeinmin) * 60)
        self.updated = Util.now_sec()
        
    def exp(self):
        """Export task fields as json string"""
        str =  "id:{}, duration:{}, start:\"{}\", name:\"{}\", type:{}, status:{},created:\"{}\""
        return "{" + str.format(self.id,self.duration,self.start,self.name,self.type,self.status,self.created) + "}"
     

    def __str__(self):
        return "{id:" + str(self.id).rjust(3) + ", dur:" + Util.format_duration(self.duration) + ", upd:" + Util.format_minutes(self.updated) +  ", name:'" + self.name + "'}"

    
    