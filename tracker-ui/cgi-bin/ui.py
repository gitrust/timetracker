#!C:\Python36\python.exe

import sys
import cgi
import Util
from cgi import *
import os

__author__      = "girust"
__copyright__   = "Copyright 2014"
__revision__    = "$Rev: 394 $"


form = cgi.FieldStorage()
doview = "yday"
doprint = "no"
URL = "http://localhost:80/cgi-bin/ui.py"
dbfile = os.getenv("USERPROFILE") + "/timer.db"

if "view" in form:
    doview = form.getfirst("view").lower()

if "doprint" in form:
    doprint = form['doprint'].value

def get_data():
        
    if doview == "day":
        data = Util.get_task_list_by_day(dbfile)
    elif doview == "week":
        data = Util.get_task_list_by_week(dbfile)
    elif doview == "dailyscrum":
        data = Util.get_task_list_dailyscrum(dbfile)
    elif doview == "yday":
        data = Util.get_task_list_yesterday(dbfile)
    elif doview == "byday":
        data = Util.get_task_list_beforeyesterday(dbfile)        
    elif doview == "today":
        data = Util.get_task_list_today(dbfile)    
    elif doview == "oneweek":
        data = Util.get_task_list_oneweek(dbfile)
    else:
        data = Util.get_task_list(dbfile)
    return data

def output_table(data):    
    print ('<div class="panel panel-default">')
    print ('<div class="panel-heading"><span class="glyphicon glyphicon-time" aria-hidden="true"></span> Task Information</div>')
    print ("<table class='table table-striped table-hover'")
    
    first_row = True    
    for row in data:

        print("<tr>")
        if first_row:
           print("<th>&nbsp;</th>")
        else:
           print("<td><input type='checkbox'></input></td>")
        for col in row:
            if first_row:
                print("<th>")
                print(to_print(col))
                print("</th>")
            else:                
                print("<td>")
                print(to_print(col))
                print("</td>")
        print("</tr>")
        first_row=False
    print ("</table>")
    print ('</div>')

def _href(link,name):
    print('<a href="%s">%s</a>' % (link,name))

def _href_btn(link,name,active=False):
    print('<li role="presentation" ')
    if active:
        print('class="active"')
    print('>')
    print('<a href="%s" >%s</a>' % (link,name))
    print('</li>')
    
def output_navigation():
    print ('<ul class="nav nav-pills">')
    # Configuration
    _href_btn(URL+"?view=task","all Tasks",(doview == "task"))
    _href_btn(URL+"?view=day","by Day",(doview == "day"))
    _href_btn(URL+"?view=byday","Before Yesterday",(doview == "byday"))    
    _href_btn(URL+"?view=yday","Yesterday",(doview == "yday"))    
    _href_btn(URL+"?view=today","Today",(doview == "today"))        
    _href_btn(URL+"?view=oneweek","1 Week",(doview == "oneweek"))
    _href_btn(URL+"?view=week","by Weeks",(doview == "week"))
    _href_btn(URL+"?view=dailyscrum","Daily Scrum",(doview == "dailyscrum"))
    _href_btn(URL+"?doprint=y&view="+doview,"Print")
    print ('</ul>')

def to_print(obj):
    return obj

def output_chart(data):
    data = Util.get_task_for_chart(dbfile,doview)
    print('<script type="text/javascript">')
    print('  google.charts.load("current", {packages:["corechart"]});')
    print('  google.charts.setOnLoadCallback(drawChart);')
    print('  function drawChart() {')
    print('      var data = google.visualization.arrayToDataTable([')
    print('       ["Task", "Hours per Day"],')
    
    for row in data:
        name = row[0]
        value = row[1]
        print("      ['" + name + "', " + value + "],")
      
    print('    ]);')
    print('   var options = { ')
    print('     title: "Activity Chart (h)",')
    print('     pieHole: 0.4,')
    print('   };')

    print('   var chart = new google.visualization.PieChart(document.getElementById("donutchart"));')
    print('   chart.draw(data, options);')
    print('  }')
    print('</script>')
    print('<div id="donutchart" style="width: 900px; height: 500px;margin:0 auto;"></div>')

def output_header():
    """ Generates a HTML GUI for configuration of svn access
    """
        
    # HTML Header
    print ("Content-Type: text/html")
    print ("")
    # HTML Site
    print ('<html><head><title>Time Tracker</title>')
    print ('<link href="/css/bootstrap.min.css" rel="stylesheet">')
    print ('<link rel="shortcut icon" href="favicon.ico" />')
    print ('<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>')
    print ('<meta charset="utf-8">')
    print ("</head>")

def output_footer():
    print('<footer class="footer">')
    print('  <div class="container">')
    print('    <p class="text-muted">Timer (%s)</p>' % __revision__)
    print('  </div>')
    print('</footer>')
    print ("</body></html>")
    
def output_body():
    """ Generates a HTML GUI for configuration of svn access
    """
    
    # list with tuples
    data = get_data()
    print ('<body>')
    print ('<div class="container">')
    # page header
    print ('<div class="page-header">')
    print ('<h1>Task information</h1>')
    print (str(len(data)-1) + " Tasks")
    print ('</div>')
    
    if not doprint in ("yes","y"):
        output_navigation()
    output_table (data)
    
    print ('<p>')
    print ('</div>')
    
    if doview in ('day','yday','today','byday','dailyscrum','oneweek'):
        output_chart(data)

    
# Execution
output_header()
output_body()
output_footer()



