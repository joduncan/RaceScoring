#!/usr/bin/python

# Program to generate scores from race results sheets
# format: Bib # , Name , age , gender , time 

import sys
import csv
import math

limit = 0 # set to zero to score everybody 
           # todo: add this as a command line argument

def score_gender( gender , results , race , factor ):

  factors = factorizer( factor )
  rank = 1 
  for name,time in results:
    if not gender.has_key( name ):
      gender[ name ] = []
    gender[ name ].append( ( race , factors.next() , rank ) )
    rank = rank + 1 

def remove_lower_scoring_duplicates( results ):
  race_score = {}
  for race,score,rank in results:
    if race_score.has_key( race ):
      if race_score[ race ] < score:
        race_score[ race ] = score,rank
    else:
      race_score[ race ] = score,rank
  return race_score.items()
      

def results_for( racer , results ):
  #if racer == "KAREN GENINATTI":
  #  print results 
  #  results = remove_lower_scoring_duplicates( results )
  #   print results
  results = remove_lower_scoring_duplicates( results )
  results.sort( key = lambda tup: tup[ 1 ][ 0 ] )
  results.reverse() 
  scores = [ result[ 1 ][ 0 ] for result in results ] 
  if len(scores) > 5:
    scores = scores[ : 5 ] 
  total = sum( scores )
  return racer , total , results 


def gender_results( gender_name , gender ):
  print "Results for" , gender_name, "racers" 
  print '<table = border = "3">'
  results = [] 
  for racer in gender.keys():
    results.append( results_for( racer , gender[ racer ] ) )
  results.sort( key = lambda tup: tup[ 1 ] )
  results.reverse()
  if limit > 0:
    results = results[ : limit ]
  rank = 1
  for r in results:
    print '<tr>'
    print '<td>' , rank , '</td>'
    print '<td>' , r[ 0 ] , '</td>' 
    print '<td>' , "%1.3f" % r[ 1 ]  , '</td>'
    for n,(p,r) in r[2]:
      print "<td>%1.3f<br>%s (%d)</td>" % ( p , n , r  )
    rank = rank + 1 
  print '</table>'
 

# a given race has a score of _n_ 
# each place is computed as 5/5+zero-based rank
#  
def factorizer( factor ):
  factor *= 5.0
  d = 5 
  while True:
    yield factor / d 
    d +=1

def main():
  sheets = sys.argv[ 1 : ] 

  males   = {}
  females = {}

  for sheet in sheets:
    with open( sheet ) as results_file:
      print >> sys.stderr , "processing" , sheet 
      event   = results_file.readline().strip()
      factor = int( results_file.readline().strip() )
      male_race   = []
      female_race = [] 
      result_reader = csv.reader( results_file , delimiter = ',' , quotechar = '"' )
      for result in result_reader:
        (name,age,gender,time) = [ result[a].strip().upper() for a in (1,2,3,-1) ]
        try:
          age = str(age)
          #print name , gender , time 
          gender = gender.upper()
          if gender in ( 'M' , 'MALE' ) :
            male_race.append( [ name , time ] )
          elif gender in ( 'F' , 'FEMALE' ):
            female_race.append( [ name , time ] )  
          else: 
            pass 
        except:
          print >> sys.stderr , "No age for " , name 
    score_gender( males   , male_race   , event , factor )
    score_gender( females , female_race , event , factor )     
  
  print '<table><tr><td valign="top">'
  gender_results( "Female" , females )
  print '</td></tr><tr><td valign="top">'
  gender_results( "Male"   , males )
  print "</td></tr></table>"

main()
