#!/usr/bin/env python

import sqlite3

sql = """create table task(
  id integer PRIMARY KEY,
  taskid integer not null,
  name char(255) not null,
  startdate int not null,
  duration integer not null,
  tasktype char(15) not null,
  taskstatus char(15) not null,
  createddate integer not null
  );"""

# delete this database first
conn = sqlite3.connect('timer.db')
c = conn.cursor()
# create table
print ("Create table...")
c.execute(sql)
conn.commit()

c.close()
