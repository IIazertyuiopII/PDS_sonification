import cPickle
import sys



def readFile(filename):
	f = open(filename,"rb")
	res = cPickle.load(f)
	f.close()
	return res

def display2tuple(t):
	a,b = t
	print a
	print b

if len(sys.argv)<2:
	print "CALL SYNTAX :"
	print "read %filename%"
	print "OR"
	print "combine %filename1% %filename2% %filename3%"
else:	
	if(sys.argv[1]=="read"):
		filename =  sys.argv[2]+".pkl"
		f = open(filename,"rb")
		res = cPickle.load(f)		
		f.close()
		if(len(res)==3):
			s1,s2,s3 = res
			print "set 1:"
			display2tuple(s1)
			print "set 2:"
			display2tuple(s2)
			print "set 3:"
			display2tuple(s3) 
		if(len(res)==2):
			display2tuple(res)

	if(sys.argv[1]=="combine"):
		filename = "combinedSets.pkl"
		set_1 = readFile(sys.argv[2]+".pkl")
		set_2 = readFile(sys.argv[3]+".pkl")
		set_3 = readFile(sys.argv[4]+".pkl")
		combinedSets = (set_1,set_2,set_3)
		f = open(filename,"wb")
		cPickle.dump(combinedSets,f)
		f.close()
		print "Export to "+filename+" finished without errors."
