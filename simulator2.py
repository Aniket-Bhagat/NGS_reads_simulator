#! /usr/bin/env python
import gzip, random, sys, numpy as np, argparse, os

parser = argparse.ArgumentParser(description='NGS reads simulator')
parser.add_argument('faFile', help='sequence file FASTA compressed gzipped')
parser.add_argument('-er', dest='err_rate',type=float, default=1.0, help='sequencig error rate (default : 1percent)')
parser.add_argument('-ch', dest='chunk',type=int, default=1000, help='chunk size (default : 1000bp)')
parser.add_argument('-o', dest='overlap',type=int, default=500, help='overlap size (default : 500bp)')
parser.add_argument('-nr', dest='reads',type=int, default=100000, help='number of reads (default : 100000)')
parser.add_argument('-rl', dest='readlen',type=int, default=50, help='read length (default : 50bp)')
parser.add_argument('--v', action="store_true", help='prints statastics of introduced errors in \'stats.csv\' file')
args = parser.parse_args()


## To divide chromosomes into chunks of 1000bp overlapping with each other by 500bp ##
def generate(div,length):
	coor = random.randint(0,div)*args.overlap
	LR = coor							# Lower Range and Upper Range of chunck
	UR = coor+args.chunk-args.readlen	# from which random start poition is selected and returned
	if length > (LR+args.readlen) and length < (UR-args.overlap): # Check for end of genome length conflicts
		return random.randint(LR,length-args.readlen)
	else:
		return	random.randint(LR,UR) # length of chunk is 1000bp
##-------------------------------------------------------------------------------------

## Error introduction (substitution) in read with probability of 1% of base calling ##
def introError(charecter, prob):
	if np.random.choice([1,0], p=prob) == 1: # probability of occuring 1(true) is 1%
		bases=['A','T','C','G','N']
		bases.remove(charecter) # remove given base
		return random.choice(bases),1 # and replace base with new base
	else :
		return charecter,0
##-------------------------------------------------------------

if __name__ == "__main__":
	# check for existances of previous files
	if os.path.isfile('./reads.fastq'):
		if raw_input('\'reads.fastq\' already exist in this directory\nDo you want to overwrite (y or n)\n') == 'y':
			pass
		else:
			sys.exit()
	if os.path.isfile('./stats.csv'):
		print '\n\'stats.csv\' already exist in this directory\nPlease Delete, Rename or Move previous file'
		sys.exit()

	## To read chromosome file except header line ##
	try:
		with gzip.open(args.faFile, 'rb') as f:
			print 'Reading Genome file...'
			genome = ''.join(f.read().splitlines()[1:-1]) # Read each line except first
			Totalength = len(genome) ## Length of genome ##
	except IOError:
		print 'Check for filename or extension given\nor file provided is not gzipped file'
		sys.exit()
	print "Done\n"
	#-------------------------------------------------------------------##
	print 'Generating reads...'

	maxdiv = Totalength/args.overlap # diveded by overlap to get overlapping window	
	p_q = [args.err_rate/100,1-args.err_rate/100] # store probability values of error rate

	## Writing result in output file ##
	with open("reads.fastq","w") as out:
		i=1; N=0; start = generate(maxdiv,Totalength)
		iniRead,Read = '',''
		mutation = []
		while (i<=args.reads):
			if N < args.readlen : # base position index less than read length
				old_base = genome[start+N] ; new_base = introError(old_base,p_q) # base calling and error introduction
				Read = Read + new_base[0] # construncting a read
				# To print stats file
				if args.v:
					iniRead = iniRead + old_base
					if new_base[1]==1:
						mutation.append(str(N+1))
				N = N+1 # increament base position index
			else:
				position = str(start+1)+':'+str(start+N+1) #store position of read
				head = '@SimulatedRead.'+str(i)+' '+position+' length='+str(N)+'\n' # Header line
				quality = ''.join([chr(random.randint(33,126)) for _ in range(len(Read))]) + '\n' # quality string charecters are ASCII values (dec 33-126)
				# write output fastq file
				out.write(head+Read+'\n'+'+\n'+quality)
				# Print verbrose (how many reads generated)
				if i%(args.reads/10) == 0:
					print i, 'reads generated'
				# To print stats file
				if args.v:
					with open('stats.csv','a') as out2:
						if len(mutation)!=0:
							out2.write('SimulatedRead.'+str(i)+'\t'+position+'\t'+iniRead+'\t'+Read+'\t'+':'.join(mutation)+'\t'+str(len(mutation))+'\n')
						mutation=[]; iniRead=''

				# Increment and reinitialization
				i=i+1; N = 0; start = generate(maxdiv,Totalength)
				Read = ''

		print 'Done.!'

##---------------------------------