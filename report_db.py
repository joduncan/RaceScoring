#!/usr/bin/python

import sqlite3
import common

import sys

conn = sqlite3.connect('results.db')
c = conn.cursor()

def sub_report( sex , range , limit , sexname ):
  print "<br><br>"

  if range == None: 
    print "All %s" % sexname
    rows = c.execute( 'select id,name,age,points from athlete where sex=? order by points desc limit ?' , ( sex , limit ) )
  else:
    (low,high) = range
    print sexname , 
    print " ages %d to %d" % range 
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
    #print >>sys.err , row 
    #row = [ i.encode( 'ascii' ) for i in row ] 
    row[ 0 ] = "#%d %s" % ( rank , row[ 0 ].encode( 'ascii' , 'replace' ) )
    res = c.execute( common.athlete_best_races , (id,) )
    for r in res:
      row.append( "%s(%d)<br>%.2f" % ( r[ 0 ] , r[ 2 ] ,  r[ 1 ] ) )
    print "<tr>"
    for r in row:
      print "<td>%s</td>" % r
    print "</tr>"
    rank += 1
  print "</table>"

age_ranges = [ None , (5,9) , (10,19) , (20,29) , (30,39) , (40,49) , (50,59) , (60,69) , (70,79) , (80,89) , (90,99) ]

age_strings = []
for a in age_ranges:
  ager = "All"
  if a <> None:
    ager = "Age %d to %d" % a 
  age_strings.append( ager )

sexes = [ [ 'F' , 'Women' , 'females' ] , [ 'M' , 'Men' , 'males' ] ] 

for sex in sexes:
  limit = 250000

  #tab_index( age_strings )
  for age_range in age_ranges:
    if age_range == None:
      ar = "all"
    else:
      ar = "%d-%d" % ( age_range[ 0 ] , age_range[ 1 ] )
    sys.stdout = open( "%s-%s.html" % ( sex[ -1 ] , ar ) , "w" ) 
    sub_report( sex[ 0 ]  , age_range , limit , sex[ -1 ] )


