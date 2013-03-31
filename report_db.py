#!/usr/bin/python

import sqlite3
import common

def print_header():
  print """<head>
           <link rel="stylesheet" href="http://jquerytools.org/media/css/tabs.css"
                 type="text/css" media="screen" />
           <link rel="stylesheet" href="http://jquerytools.org/media/css/tabs-panes.css"
                 type="text/css" media="screen" />
           <script src="http://cdn.jquerytools.org/1.2.7/full/jquery.tools.min.js"></script>
           </head>
           <body>"""



def tab_index( content_titles ):
  print """<div class="box" >
           <!-- the tabs -->
           <ul class="tabs">"""
  for c in content_titles:
    print """<li><a href="#">%s</a></li>""" % c 
  print """</ul>"""

def start_content():
  print """<!-- tab "panes" -->
           <div class="panes">"""


conn = sqlite3.connect('results.db')
c = conn.cursor()


def sub_report( sex , range , limit ):
  print "<br><br>"

  if range == None: 
    rows = c.execute( 'select id,name,age,points from athlete where sex=? order by points desc limit ?' , ( sex , limit ) )
  else:
    (low,high) = range
    print "Ages %d to %d" % range 
    rows = c.execute( 'select id,name,age,points from athlete where sex=? and age>= ? and age <= ? order by points desc limit ?' , 
                      ( sex , low , high , limit ) )
  r2 = [] 
  for row in rows:
    r2.append( list( row ) )
  print '<table border="3">'
  rank = 1
  for row in r2:
    row[ 3 ] = "%.2f" % row[ 3 ]
    id = row[ 0 ]
    row = row[ 1: ]
    row = [ str(i) for i in row ] 
    row[ 0 ] = "#%d %s" % ( rank , row[ 0 ] )
    res = c.execute( common.athlete_best_races , (id,) )
    for r in res:
      row.append( "%s(%d)<br>%.2f" % ( r[ 0 ] , r[ 2 ] ,  r[ 1 ] ) )
    print "<tr>"
    for r in row:
      print "<td>%s</td>" % r
    print "</tr>"
    rank += 1
  print "</table>"

age_ranges = [ None , (5,9) , (10,19) , (20,29) , (30,39) , (40,49) , (50,59) , (60,69) , (70,79) , (80,89) , (90,98) ]

sexes = [ 'F' , 'M' ] 

print_header()
tab_index( [ "Women" , "Men" ] )
start_content()

for sex in sexes:
  print "<div>"
  limit = 250

  for age_range in age_ranges:
    sub_report( sex , age_range , limit )
    limit = 10 
  print "</div>"

print """</div>

<script>
// perform JavaScript after the document is scriptable.
$(function() {
    // setup ul.tabs to work as tabs for each div directly under div.panes
    $("ul.tabs").tabs("div.panes > div");
});

</script>
"""

