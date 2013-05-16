#!/usr/bin/python

# Program to generate scores from race results sheets
# format: Bib # , Name , age , gender , time 

import sys
import os
import csv
import math
import sqlite3
import common


conn = sqlite3.connect('results.db')
c = conn.cursor()


#
# go through the database and elimintate the racers/results for 
# athletes that have fewer than three races
#


def clean_db():
  res = c.execute( 'select athlete,count(*) from results group by athlete' ) 
  to_del = []
  for (id,count) in res:
    if count < 3:
      to_del.append( id )
  for td in to_del:
    c.execute( "delete from results where athlete=?" ,(td,))
    c.execute( "delete from athlete where id=?" , (td,))
  c.execute( "vacuum" ) 
  conn.commit()


def adjust_races():
  r = c.execute( "select id from athlete" )
  a = []
  for ath in r:
    a.append( ath[ 0 ] ) 

  for ath in a:
    res = c.execute( 'select race.name,max(points),rank from results join race on race = race.id where athlete = ? group by race.name order by max(points) desc' , (ath,))
    races = []
    for r in res:
      races.append( r[ 0 ] )
    race_count = len( races )
    print ath , race_count , races 

#clean_db()
adjust_races()

