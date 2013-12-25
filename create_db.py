#!/usr/bin/python

# Program to generate scores from race results sheets
# format: Bib # , Name , age , gender , time 

import sys
import os
import csv
import math
import sqlite3
import common
import datetime

try:
  os.remove( 'results.db' )
except:
  pass
conn = sqlite3.connect('results.db')
c = conn.cursor()

c.execute( "create table race    ( id INTEGER PRIMARY KEY AUTOINCREMENT  , name string , date date , factor integer , url string )" )
c.execute( "create table athlete ( id INTEGER PRIMARY KEY AUTOINCREMENT  , name string , sex string , age integer , points float )" )
c.execute( "create index athname on athlete(name)" ) # cut creation time from 50.8 to 30.8
c.execute( "create table results  ( id INTEGER PRIMARY KEY AUTOINCREMENT  , race integer , athlete integer , rank integer , points float )" )
c.execute( "create index resath on results(athlete)" ) #cut creation time from 30.8 to 1.26 (!!) 

def find_racer( name , age , gender ):
  try:
    age = int( age )
    c.execute( "select id , age from athlete where name=? and sex=? and ( ( age >= ? ) and ( age <= ? ) or age is null )" , 
               ( name , gender , age - 1 , age + 1 ) ) 
  except:
    c.execute( "select id , age from athlete where name=? and sex=?" , ( name , gender  ) )
  try:
    row = c.fetchone()
    if isinstance( age , int ) and row[ 1 ] == None:
      c.execute( "update athlete set age = ? where id = ?" , ( age , row[ 0 ] ) )
    return row[ 0 ]
  except:
    return None

def try_add( name , age , gender ):
  id = find_racer( name , age , gender )
  if id <> None:
    return id
  try:
    age = int( age )
    c.execute( "insert into athlete( name , sex , age ) values( ? , ? , ? )" , ( name , gender , age ) )
  except:
    c.execute( "insert into athlete( name , sex ) values( ? , ? )" , ( name , gender ) )
  return c.lastrowid

 
def add_gender( race_id , racers ):
  rank = 1 
  seen = {}
  for racer in racers:
    if not seen.has_key( racer ):
      c.execute( "insert into results(  race , athlete , rank ) values(?,?,?)" , ( race_id , racer , rank ) )
      rank = rank + 1 
      seen[ racer ] = 1
    else:
      print "Skipping" , race_id , racer , rank
   


def main():
  sheets = os.popen( "ls data/*.csv" ).readlines()

  for sheet in sheets:
    sheet = sheet.strip()
    with open( sheet ) as results_file:
      print >> sys.stderr , "processing" , sheet 
      event   = results_file.readline().strip()

      dp = [ int(x) for x in results_file.readline().strip().split('-') ]
      date = datetime.date( dp[0] , dp[1], dp[2]  )

      #so much ugly code, especially this:
      fs = results_file.readline().strip()
      url = fs
      fs = results_file.readline().strip()
      factor = int( fs )

      c.execute( "insert into race(name,factor,date,url) values(?,?,?,?)" , ( event , factor , date , url ) )
      race_id = c.lastrowid

      male_race   = []
      female_race = [] 
      result_reader = csv.reader( results_file , delimiter = ',' , quotechar = '"' )
      for result in result_reader:
        result = [unicode(cell, 'utf-8') for cell in result]
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
      add_gender( race_id , male_race )
      add_gender( race_id , female_race )

main()
conn.commit()
