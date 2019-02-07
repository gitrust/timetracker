#!C:\Python36\python.exe

import sys
import cgi
import Util
from cgi import *
import os

__author__      = "girust"
__revision__    = "$Rev: 394 $"

PORT = 8080
form = cgi.FieldStorage()
views = ('day','yday','today','byday','dailyscrum','oneweek')
view = "yday"
viewchart = True
doprint = "no"
URL = "http://localhost:" + str(PORT) + "/cgi-bin/ui.py"
dbfile = os.getenv("USERPROFILE") + "/timer.db"

if "view" in form:
    view = form.getfirst("view").lower()

if "doprint" in form:
    doprint = form['doprint'].value

def get_data():
        
    if view == "day":
        data = Util.get_task_list_by_day(dbfile)
    elif view == "week":
        data = Util.get_task_list_by_week(dbfile)
    elif view == "dailyscrum":
        data = Util.get_task_list_dailyscrum(dbfile)
    elif view == "yday":
        data = Util.get_task_list_yesterday(dbfile)
    elif view == "byday":
        data = Util.get_task_list_beforeyesterday(dbfile)        
    elif view == "today":
        data = Util.get_task_list_today(dbfile)    
    elif view == "oneweek":
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
    _href_btn(URL+"?view=task","all Tasks",(view == "task"))
    _href_btn(URL+"?view=day","by Day",(view == "day"))
    _href_btn(URL+"?view=byday","Before Yesterday",(view == "byday"))    
    _href_btn(URL+"?view=yday","Yesterday",(view == "yday"))    
    _href_btn(URL+"?view=today","Today",(view == "today"))        
    _href_btn(URL+"?view=oneweek","1 Week",(view == "oneweek"))
    _href_btn(URL+"?view=week","by Weeks",(view == "week"))
    _href_btn(URL+"?view=dailyscrum","Daily Scrum",(view == "dailyscrum"))
    _href_btn(URL+"?doprint=y&view="+view,"Print")
    print ('</ul>')

def to_print(obj):
    return obj

def output_chart(data):
    data = Util.get_task_for_chart(dbfile,view)
    print('<script type="text/javascript">')
    print('  google.charts.load("current", {packages:["corechart"]});')
    print('  google.charts.setOnLoadCallback(drawChart);')
    print('  function drawChart() {')
    print('      var data = google.visualization.arrayToDataTable([')
    print('       ["Task", "Hours per Day"],')
    
    for row in data:
      name = row[0]
      value = row[1]
      print("      ['"+name+"', "+value+"],")
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
    
    if viewchart and view in views:
            output_chart(data)

    
# Execution
output_header()
output_body()
output_footer()



