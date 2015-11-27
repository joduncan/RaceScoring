#!/usr/bin/python

import sqlite3
import common

conn = sqlite3.connect(common.db)
c = conn.cursor()

def compute_runner_score():
  rows = c.execute( "select id from athlete" )
  ids = []
  for row in rows:
    ids.append( row[ 0 ] )
  for id in ids:
    r2 = c.execute( common.athlete_best_races , (id, common.races_that_count ) )
    score = 0
    for r in r2:
      score += r[ 1 ]
    c.execute( "update athlete set points = ? where id = ?" , ( score , id ) )

def score_gender( racers , race_id , factor ):
  score = common.factorizer( factor )
  rank = 1 
  for racer in racers:
    #c.execute( "insert into results(  race , athlete , rank , points ) values(?,?,?,?)" , ( race_id , racer , rank , score.next() ) )
    c.execute( "update results set points = ? where id = ?" , ( score.next() , racer ) )
    rank = rank + 1 

def score_races():
  rows = c.execute( "select id , factor from race" )
  rids = [ ( row[ 0 ] , row[ 1 ] ) for row in rows ]
  for race_id,factor in rids:
    for gender in [ 'M' , 'F' ]:
      racers = c.execute( "select results.id from results join athlete on results.athlete = athlete.id where race = ? and sex = ?" ,
                            ( race_id , gender ) )
      racers = [ r[0] for r in racers ]
      score_gender( racers , race_id , factor ) 

score_races()
compute_runner_score()
conn.commit()


