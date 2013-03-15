#!/usr/bin/python

# Program to generate scores from race results sheets
# format: Bib # , Name , age , gender , time 

import csv

with open( "esbru_pre.txt" ) as results_file:
  result_reader = csv.reader( results_file , delimiter = ',' , quotechar = '"' )
  for result in result_reader:
    result = [ a.strip().upper() for a in result ]
    bib,last,first,gen_age,state,nation,time = result
    gender,age = gen_age[0],gen_age[1:]
    name = first + " " + last
    if state == '':
      gender = 'x'
    res = [ '"%s"' % a for a in [ bib,name,age,gender,time ] ]
    print ",".join( res )

