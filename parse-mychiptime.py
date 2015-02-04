import sys

inl = open( sys.argv[1] ).readlines()
inl = [ i.split("\t") for i in inl ]

for i in range( len( inl ) / 3 ):
    i1,i2,i3=inl[i*3:i*3+3]
    number = i1[2]
    name = i1[3]+" "+i1[4]
    age='' #i3[6]
    #print i3[9]
    sex = sys.argv[2]
    time = i1[1]
    print ",".join( [number,name,age,sex] )
    
