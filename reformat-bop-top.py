import csv


lines = open( "bop-top-triple1.csv" )
for line in lines:
  if line[0]<>',':
    print line.strip()
