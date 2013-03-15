import sys

lines = sys.stdin.readlines()

for line in lines:
  line = line.split( "," )
  (fn,ln)=line[1],line[2]
  fn = fn[ 1:-1 ]
  ln = ln[ 1:-1 ]
  line = [ line[ 0 ] , '"' + fn + ' ' + ln + '"' ] + line[ 3: ]
  line = ",".join( line ) 
  print line.strip()
