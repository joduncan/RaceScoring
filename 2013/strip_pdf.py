import sys

for line in sys.stdin.readlines():
  line = line.strip()
  line = line[ line.find( '(' ) + 1 : ]
  line = line[ : line.find( ')' ) ]
  print line 
