#!/usr/bin/python

import sqlite3
import common
import time 
import sys

conn = sqlite3.connect('results.db')
c = conn.cursor()

def sub_report( sex , range , limit , sexname ):
  print "<br><br>"

  category = "Open"
  ignores = open( "data/ignores").readlines()
  ignores = [ i.strip().upper() for i in ignores ]

  if range == None: 
    print "All %s" % sexname
    rows = c.execute( 'select id,name,age,points from athlete where sex=? order by points desc limit ?' , ( sex , limit ) )
  else:
    (low,high) = range
    category = "%d-%d" % ( low , high )
    print sexname , 
    print " ages %d to %d" % range 
    rows = c.execute( 'select id,name,age,points from athlete where sex=? and age>= ? and age <= ? order by points desc limit ?' , 
                      ( sex , low , high , limit ) )
  r2 = [] 
  for row in rows:
    if not (row[1] in ignores):
      r2.append( list( row ) )
  print '<table border="3">'
  rank = 1
  for row in r2:

    points = row[3]
    row[ 3 ] = "%.2f" % points
    id = row[ 0 ]
    row = row[ 1: ]

    name = row[ 0 ].encode( 'ascii' , 'replace' )
    row[ 0 ] = "#%d %s" % ( rank ,  name )
    res = c.execute( common.athlete_best_races , (id,100) )
    for r in res:
      row.append( "%s(%d)<br>%.2f" % ( r[ 0 ] , r[ 2 ] ,  r[ 1 ] ) )
    print "<tr>"
    col = 1
    for r in row:
      color = 'White'
      if col > 3:
        color = 'AliceBlue'
      if col > 8:
        color = 'Crimson'
      print '<td bgcolor="%s">%s</td>' % ( color , r ) 
      col = col + 1 
    print "</tr>"
    c.execute( "insert into sheets(name,sex,category,rank,points,results) values(?,?,?,?,?,?)" , (name,sex,category,rank,points,"") )
    rank += 1
  print "</table>"
  conn.commit()

age_ranges = [ None , (5,9) , (10,19) , (20,29) , (30,39) , (40,49) , (50,59) , (60,69) , (70,79) , (80,89) , (90,99) ]

age_strings = []
for a in age_ranges:
  ager = "All"
  if a <> None:
    ager = "Age %d to %d" % a 
  age_strings.append( ager )

sexes = [ [ 'F' , 'Women' , 'females' ] , [ 'M' , 'Men' , 'males' ] ] 

gs = open( "html/genders.html" , "w" )
print >> gs , "Rankings as of " + time.strftime("%x")
for l in open( "genders.templ" ).readlines():
  print >>gs , l 

for sex in sexes:
  limit = 250000

  #tab_index( age_strings )
  for age_range in age_ranges:
    if age_range == None:
      ar = "all"
    else:
      ar = "%d-%d" % ( age_range[ 0 ] , age_range[ 1 ] )
    sys.stdout = open( "html/%s-%s.html" % ( sex[ -1 ] , ar ) , "w" ) 
    sub_report( sex[ 0 ]  , age_range , limit , sex[ -1 ] )


###
#
# Now generate a list of races that people can look at
# 
###
rows = c.execute( "select name ,date , url from race group by name order by date" )
out = open( "html/race_list.html" , "w" )
for name,date,url in rows:
  print >>out , '<a href="%s">%s</a> %s<br>' % ( url , name , date )


