#!/usr/bin/env python

""" util.py with static functions """

__author__      = "gitrust"
__revision__    = "$Rev: 229 $"

import datetime
import time


try:
    import sqlite3
except ImportError:
    print("Could not import sqlite3")
    
def format_duration(sec):
    """ Format duration in seconds
    
    Args:
      sec (int): seconds since 1970...
      
    """
    hours,remainder = divmod(sec,3600)
    min = remainder//60
    ftime = "%s:%s" % (str(hours).rjust(2,'0'),str(min).rjust(2,'0'))
    return str(ftime).rjust(5)
    
def format_minutes(ts):
    """Format time in HH:MM
    
    Args:
      ts (int) seconds since begin of epoch
    """
    time = datetime.datetime.fromtimestamp(ts)
    return str(time.strftime("%H:%M"))

def format_starttime(tasklist):
    """Calculate start time using starttime for an 8hour day
    
    Args:
      tasklist: all tasks to calculate starttime from
    """
    created = 0
    for id in tasklist:
        # get the first task
        if created == 0 or tasklist[id].created < created:
            created = tasklist[id].created
    return format_minutes(created);
    
def format_endtime(tasklist):
    """Calculate end time using starttime for an 8hour day
    
    Args:
      tasklist: all tasks to calculate starttime from
    """
    paused = 0
    worked = 0
    created = 0
    now = now_sec()
    
    for id in tasklist:
        task = tasklist[id]
        # get the first task
        if created == 0 or task.created < created:
            created = task.created
            
        # get work time (ungleich pause type)
        if task.type == 1:
            paused += task.duration
        else:
            worked  += task.duration
    
    # 8hours
    worktarget =  (8 * 60 * 60)
    # 30min
    pausetarget = (30 * 60)
    
    pausedelta = 0
    if paused < pausetarget:
        pausedelta = pausetarget - paused
        
    # overworked
    if (worktarget - worked) <   0:
        return "overtime"
    else:
        return format_minutes(now + (worktarget - worked) + pausedelta)
    
def now_sec():
    """Timestamp in seconds since 1970"""
    now = time.time()
    return int(now)

def export_to_db(data, dbfile):
    """Export data from dictionary data to sqlite database dbfile
    
    Args:
      data (list with dictionaries)   - list with dictionary data
      dbfile (str) - path to sqlite database file
    """
    
    list_with_tuples=[]
    
    for d in data:
        tup = (d["id"],d["name"],d["start"],d["duration"],d["type"],d["status"],d["created"])
        list_with_tuples.append(tup)
    
    db = sqlite3.connect(dbfile)
    cursor = db.cursor()
    
    cursor.executemany('''INSERT INTO task(taskid,name,startdate,duration,tasktype,taskstatus,createddate)  VALUES(?,?,?,?,?,?,?)''',list_with_tuples)
    db.commit()    
    db.close()
    