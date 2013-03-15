#!/usr/bin/python

# Program to generate scores from race results sheets
# format: Bib # , Name , age , gender , time 

import sys
import os
import csv
import math
import sqlite3

os.remove( 'results.db' )
conn = sqlite3.connect('results.db')
c = conn.cursor()

c.execute( "create table race    ( id INTEGER PRIMARY KEY AUTOINCREMENT  , name string )" )
c.execute( "create table athlete ( id INTEGER PRIMARY KEY AUTOINCREMENT  , name string , sex string , age integer , points float )" )
c.execute( "create table results  ( id INTEGER PRIMARY KEY AUTOINCREMENT  , race integer , athlete integer , rank integer , points float )" )

def find_racer( name , age , gender ):
  c.execute( "select id from athlete where name=? and sex=?" , ( name , gender ) )
  try:
    row = c.fetchone()
    return row[ 0 ]
  except:
    return None

def try_add( name , age , gender ):
  id = find_racer( name , age , gender )
  if id <> None:
    return id
  c.execute( "insert into athlete( name , sex , age ) values( ? , ? , ? )" , ( name , gender , age ) )
  return c.lastrowid

# a given race has a score of _n_ 
# each place is computed as 5/5+zero-based rank
#  
def factorizer( factor ):
  factor *= 5.0
  d = 5 
  while True:
    yield factor / d 
    d +=1

def score_gender( racers , race_id , factor ):
  score = factorizer( factor )
  rank = 1 
  for racer in racers:
    c.execute( "insert into results(  race , athlete , rank , points ) values(?,?,?,?)" , ( race_id , racer , rank , score.next() ) )
    rank = rank + 1 

def main():
  sheets = sys.argv[ 1 : ] 

  for sheet in sheets:
    with open( sheet ) as results_file:
      print >> sys.stderr , "processing" , sheet 
      event   = results_file.readline().strip()
      c.execute( "insert into race(name) values(?)" , ( event , ) )
      race_id = c.lastrowid

      factor = int( results_file.readline().strip() )
      male_race   = []
      female_race = [] 
      result_reader = csv.reader( results_file , delimiter = ',' , quotechar = '"' )
      for result in result_reader:
        (name,age,gender,time) = [ result[a].strip().upper() for a in (1,2,3,-1) ]
        gender = gender.upper()
        if gender == 'MALE':
          gender = 'M'
        if gender == 'FEMALE':
          gender = 'F'
        athlete_id = try_add( name , age , gender )
        try:
          age = str(age)
          #print name , gender , time 
          gender = gender.upper()
          if gender == 'M':
            male_race.append( athlete_id )
          elif gender == 'F':
            female_race.append( athlete_id )  
          else: 
            pass 
        except:
          print >> sys.stderr , "No age for " , name 
    score_gender( male_race   , race_id , factor )
    score_gender( female_race , race_id , factor )     


def compute_runner_score():
  rows = c.execute( "select id from athlete" )
  ids = []
  for row in rows:
    ids.append( row[ 0 ] )
  for id in ids:
    r2 = c.execute( "select race.name,max(points) from results join race on race = race.id where athlete = ? group by race.name order by max(points) desc limit 5" , (id, ) )
    score = 0
    for r in r2:
      score += r[ 1 ]
    c.execute( "update athlete set points = ? where id = ?" , ( score , id ) )
      
  
main()
conn.commit()
compute_runner_score()
conn.commit()
