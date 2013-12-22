#!/usr/bin/python


import sqlite3
import common
import math
import sys

delta = int( sys.argv[1] )

conn = sqlite3.connect('results.db')
c = conn.cursor()

# get a list of ALL athletes
aids = c.execute( "select id from athlete" )
aids = [ a[ 0 ] for a in aids ]

# get a list of race id's and names
rids = c.execute( "select name,factor from race" )
rh = {}
for rid in rids:
  rh[ rid[ 0 ] ] = [ rid[ 1 ] , 0 ]


# loop through all athletes.  If an athlete did more than one race, panalize the first 1/2 
# boost the last 1/2

for aid in aids:
  res = c.execute( common.athlete_best_races , ( aid , 100 ) )
  res = [ r[0] for r in res ]
  les = len( res )
  if les > 2:
    ls = les / 2
    overrated = res[:ls]
    underrated = res[ -ls :] 
    for i in overrated:
      rh[i][1] = rh[i][1] - 1 
    for i in underrated:
      rh[i][1] = rh[i][1] + 1 
      
for r in rh.keys():
  bonus = rh[r][1]
  print r , bonus
  if bonus <> 0:
    c.execute( "update race set factor = ? where name = ?" , ( rh[ r ][ 0 ] + math.copysign( delta , bonus ) , r ) )
conn.commit()

