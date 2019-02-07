#!/usr/bin/env python

""" Util.py with helper functions """

__author__      = "gitrust"
__revision__    = "$Rev: 394 $"

import datetime
import time
import urllib

try:
    import sqlite3
except ImportError:
    print("ERROR: could not import sqlite3")

SQL_QUERY = {
    "today" : """
     SELECT id, taskid, name, duration, startdate, tasktype, taskstatus,createddate
     FROM Task 
     WHERE datetime(startdate,'unixepoch') >= datetime('now','start of day')
     ORDER BY startdate desc
     """,
     "yesterday" : """
     SELECT  name, sum(duration)
     FROM Task 
     WHERE datetime(startdate,'unixepoch') >= datetime('now','start of day','-1 day')
     GROUP BY name
     ORDER BY startdate desc
     """,
     "oneweek": """
     SELECT name, sum(duration), strftime("%Y.%m.%d",datetime(createddate,'unixepoch')) as time
     FROM Task 
     WHERE datetime(startdate,'unixepoch') >= datetime('now','start of day','-7 day')
     AND tasktype != 'PAUSE'
     group by time, name
     ORDER BY startdate desc
     """,
     "beforeyesterday": """
     SELECT name, sum(duration)
     FROM Task 
     WHERE datetime(startdate,'unixepoch') >= datetime('now','start of day','-2 day')
     AND datetime(startdate,'unixepoch') < datetime('now','start of day','-1 day')
     GROUP BY name
     ORDER BY startdate desc
     """,
     "dailyscrum13": """
     SELECT  name, sum(duration)
     FROM Task 
     WHERE datetime(startdate,'unixepoch') > datetime('now','start of day','-13 hours')
     GROUP BY name
     ORDER BY startdate desc
     """,
      "dailyscrum61": """
     SELECT name, sum(duration)
     FROM Task 
     WHERE datetime(startdate,'unixepoch') > datetime('now','start of day','-61 hours')
     GROUP BY name
     ORDER BY startdate desc
     """,
     "byday": """
     SELECT  strftime("%Y.%m.%d",datetime(createddate,'unixepoch')) as time, sum(duration)
     FROM Task 
     GROUP BY  time
     ORDER BY time desc
     """,
     "byweek": """
     SELECT  strftime("%Y - %W",datetime(createddate,'unixepoch')) as time, sum(duration)
     FROM Task 
     GROUP BY  time
     ORDER BY time desc
     """,
     "tasklist" : """
     SELECT id, taskid, name, duration, startdate, tasktype, taskstatus,createddate
     FROM Task 
     ORDER BY startdate desc
     """
}

SQL_CHARTQUERY = {
    "today": "WHERE datetime(startdate,'unixepoch') >= datetime('now','start of day')",
    "yday" : "WHERE datetime(startdate,'unixepoch') >= datetime('now','start of day','-1 day')",
    "oneweek": "WHERE datetime(startdate,'unixepoch') >= datetime('now','start of day','-7 day') AND tasktype != 'PAUSE'",
    "byday": "WHERE datetime(startdate,'unixepoch') >= datetime('now','start of day','-2 day') AND datetime(startdate,'unixepoch') < datetime('now','start of day','-1 day')",
    "dailyscrum-61": "WHERE datetime(startdate,'unixepoch') > datetime('now','start of day','-61 hours')",
    "dailyscrum-13": "WHERE datetime(startdate,'unixepoch') > datetime('now','start of day','-13 hours')"
}

def format_duration(sec):
    """ Format duration in seconds
    
    Args:
      sec (int): seconds since 1970...
      
    """
    hours,remainder = divmod(sec,3600)
    min = remainder//60
    ftime = "%s:%s" % (hours,str(min).rjust(2,'0'))
    return str(ftime).rjust(5)

def format_name(str):
    return str
    
def format_minutes(ts):
    """Format time in HH:MM
    
    Args:
      ts (int) seconds since begin of epoch
    """
    time = datetime.datetime.fromtimestamp(ts)
    return str(time.strftime("%H:%M"))

def format_time(ts):
    """Format time in HH:MM
    
    Args:
      ts (int) seconds since begin of epoch
    """
    time = datetime.datetime.fromtimestamp(ts)
    return str(time.strftime("%d.%m.%y %H:%M"))
    
def now_sec():
    """Timestamp in seconds since 1970"""
    now = time.time()
    return int(now)

def get_dailyscrum_offset():
    offset = -13
    weekday = datetime.datetime.today().weekday()
    if weekday == 0:
        offset = -61
    return offset
    
def get_task_list_today(dbfile):
    """Returns a list with data as tuples"""
    db = sqlite3.connect(dbfile)
    cursor = db.cursor()
    
    offset = get_dailyscrum_offset()
    
    data = [("#","Task Id","Task Description","Duration (h)","Update","Type","Status","Created")]
    cursor.execute(SQL_QUERY["today"])
    
    rows = cursor.fetchall()
    for row in rows:
        id = row[0]
        tid = row[1]
        name = format_name(row[2])
        dur = format_duration(row[3])
        start = format_time(row[4])
        type = row[5]
        status = row[6]
        created = format_time(row[7])
        
        data.append((id,tid,name,dur,start,type,status,created))
        
    db.close()
    return data
	
def get_task_list_yesterday(dbfile):
    """Returns a list with data as tuples"""
    db = sqlite3.connect(dbfile)
    cursor = db.cursor()
    
    data = [("Task","Duration (h)")]
    cursor.execute(SQL_QUERY["yesterday"])
    
    rows = cursor.fetchall()
    for row in rows:
        name = format_name(row[0])
        dur = format_duration(row[1])
        
        data.append((name,dur))
        
    db.close()
    return data
    
def get_task_for_chart(dbfile,view):
    """Returns a list with data as tuples"""
    db = sqlite3.connect(dbfile)
    cursor = db.cursor()
    
    # workaround for dailyscrum sql syntax
    if view == "dailyscrum":
        view += str(get_dailyscrum_offset())
        
    if view not in SQL_CHARTQUERY:
        return []
        
    whereclause = SQL_CHARTQUERY[view]
    sqlclause = "SELECT  lower(name), Sum(duration) as dur FROM Task " + whereclause + " GROUP BY lower(name) ORDER BY dur desc"
    data = []
    cursor.execute(sqlclause)
    
    rows = cursor.fetchall()
    for row in rows:
        name = str(row[0])
        # convert to minutes
        dur = str(float(row[1])/60/60)
        
        data.append((name,dur))
        
    db.close()
    return data
    
def get_task_list_oneweek(dbfile):
    """Returns a list with data as tuples"""
    db = sqlite3.connect(dbfile)
    cursor = db.cursor()
    
    # header
    data = [("Task Description","Duration (h)","Created")]
    
    cursor.execute(SQL_QUERY["oneweek"])
    
    rows = cursor.fetchall()
    for row in rows:
        name = format_name(row[0])
        dur = format_duration(row[1])
        time = row[2]
        data.append((name,dur,time))
        
    db.close()
    return data    

def get_task_list_beforeyesterday(dbfile):
    """Returns a list with data as tuples"""
    db = sqlite3.connect(dbfile)
    cursor = db.cursor()
    
    
    data = [("Task","Dauer (h)")]
    cursor.execute(SQL_QUERY["beforeyesterday"])
    
    rows = cursor.fetchall()
    for row in rows:
        name = format_name(row[0])
        dur = format_duration(row[1])
        
        data.append((name,dur))
        
    db.close()
    return data    
	
	
def get_task_list_dailyscrum(dbfile):
    """Returns a list with data as tuples"""
    db = sqlite3.connect(dbfile)
    cursor = db.cursor()
    
    offset = -13
    weekday = datetime.datetime.today().weekday()
    if weekday == 0:
        offset = -61
    
    data = [("Task","Duration (h)")]
    # TODO set hours offset into SQL statement dynamically
    
    if offset == -13:
        cursor.execute(SQL_QUERY["dailyscrum13"])
    else:
        cursor.execute(SQL_QUERY["dailyscrum61"])
    
    rows = cursor.fetchall()
    for row in rows:
        name = format_name(row[0])
        dur = format_duration(row[1])
        
        data.append((name,dur))
        
    db.close()
    return data
    
def get_task_list(dbfile):
    """Returns a list with data as tuples"""
    db = sqlite3.connect(dbfile)
    cursor = db.cursor()
    
    data = [("#","Task Id","Task Description","Duration (h)","Update","Type","Status","Created")]
    cursor.execute(SQL_QUERY["tasklist"])
    
    rows = cursor.fetchall()
    for row in rows:
        id = row[0]
        tid = row[1]
        name = format_name(row[2])
        dur = format_duration(row[3])
        start = format_time(row[4])
        type = row[5]
        status = row[6]
        created = format_time(row[7])
        
        data.append((id,tid,name,dur,start,type,status,created))
        
    db.close()
    return data

    
def get_task_list_by_week(dbfile):
    """Returns a list with data as tuples"""
    db = sqlite3.connect(dbfile)
    cursor = db.cursor()
    
    data = [("Week","Duration with pause (h)")]
    cursor.execute(SQL_QUERY["byweek"])
    
    rows = cursor.fetchall()
    for row in rows:
        date = row[0]
        dur = format_duration(row[1])
        data.append((date,dur))
    db.close()
    return data
    
def get_task_list_by_day(dbfile):
    """Returns a list with data as tuples"""
    db = sqlite3.connect(dbfile)
    cursor = db.cursor()
    
    data = [("Date","Duration with pause (h)")]
    cursor.execute(SQL_QUERY["byday"])
    
    rows = cursor.fetchall()
    for row in rows:
        date = row[0]
        dur = format_duration(row[1])
        data.append((date,dur))
    db.close()
    return data
    

def get_dummy_list():
    l=[]
    l.append(("Task","Description", "Content","Date"))
    l.append(("Task1","Description1", "Content","2.2.2014"))
    l.append(("Task2","Description2", "Description","1.1.2014"))
    l.append(("Task3","Description3", "Content","1.2.2014"))
    l.append(("Task4","Description4", "Content","3.3.2014"))
    l.append(("Task5","Description5", "Content","5.5.2014"))
    return l
    
def export_to_db(data, dbfile):
    """Export data from dictionary data to sqlite database dbfile
    
    Args:
      data (list with dictionaries)   - list with dictionary data
      dbfile (str) - path to sqlite database file
    """
    list_with_tuples=[]
    # TODO convert data into list with tuples
    for d in data:
        tup = (d["id"],d["name"],d["start"],d["duration"],d["type"],d["status"],d["created"])
        list_with_tuples.append(tup)
    
    db = sqlite3.connect(dbfile)
    cursor = db.cursor()
    
    cursor.executemany('''INSERT INTO task(taskid,name,startdate,duration,tasktype,taskstatus,createddate)
                      VALUES(?,?,?,?,?,?,?)''',list_with_tuples)
    db.commit()    
    db.close()

    