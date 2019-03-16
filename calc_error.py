#! /usr/bin/env python
import gzip,sys,re

arg = sys.argv

with gzip.open(arg[1],'rb') as f:
	File = f.read().splitlines()
	origins = {}
	for i in range(0,len(File),4):
		line = File[i].split(' ')
		key = line[0][1:]
		value = line[1].split(':')[0]
		origins[key]=value

with open(arg[2]) as f:
	File = f.read().splitlines()
	count = 0; mapped=0; umapped=0
	for line in File:
		col = line.split('\t')
		if re.search('\tXA:',line):
			count = count + 1
			mapped = mapped + 1
		elif col[3] != '0':
			mapped = mapped + 1
			if origins[col[0]] != col[3]:
				count = count + 1
				# print col[0], origins[col[0]], col[3]
		else:
			umapped = umapped + 1

print count, 'reads mapped on genome position other than where it originated from'
print mapped, 'reads mapped to genome'
print umapped, 'reads not mapped to genome\n'

ErrorRate = (float(count)/mapped)*100
print("%2.f" %(ErrorRate))+'% Error Rate (reads mapped on genome position other than where it originated from)'
