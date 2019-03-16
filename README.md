# NGS Reads Simulator
---------------
Author : Aniket Bhagat
--
Note: All the code is mainly implemented in Python2.7.12
1. Human Chr17 (GRCh38) Downloaded from ensemble ftp [link](http://ftp.ensembl.org/pub/release-95/fasta/homo_sapiens/dna/).
2. Chromosome is divided in chunks of 1000bp (overlapping adjecent chuck with 500bp)
3. Random chunck is selected from which random index is choosen for read of 50bp.
4. Quality values randomly generated for 50 characters (ASCII - 33 to 126).
5. Random errors are introduced in read with error rate 1% (probablity 0.01).
6. Only substituions are introduced as errors.
7. Reads aligned back to reference chromosome.
8. Error rate calculated (read aligned to a part of the genome other than where it originated from).
-----
# How to use
Give user permissions before running:
`$ chmod 777 simulator2.py`

For help:
```sh
$ ./simulator2.py -h

usage: simulator2.py [-h] [-er ERR_RATE] [-ch CHUNK] [-o OVERLAP] [-nr READS]
                     [-rl READLEN] [--v]
                     faFile

NGS reads simulator

positional arguments:
  faFile        sequence file FASTA compressed gzipped

optional arguments:
  -h, --help    show this help message and exit
  -er ERR_RATE  sequencig error rate (default : 1%)
  -ch CHUNK     chunk size (default : 1000bp)
  -o OVERLAP    overlap size (default : 500bp)
  -nr READS     number of reads (default : 100000)
  -rl READLEN   read length (default : 50bp)
  --v           prints statastics of introduced errors in 'stats.csv' file
```
  Default values are assigned according to given exercise

To test with given chromosome file 'GRCh38_chromosome17.fa.gz' run following command: 
`$ time ./simulator2.py --v GRCh38_chromosome17.fa.gz`

After successfully running we get two files : *reads.fastq* & *stats.csv*
# 1. reads.fastq 
    File contains simulated read
  Header : 'SimulaterdRead number', 'Start and End coordinates', 'Length'
Copmress *reads.fastq* using gzip : `$ gzip -k reads.fastq`
# 2. stats.csv
    Tab seperated file contaning information about error introduced in reads
    (reads where errors are not introduced are not present here)
    columns in file:
        1. Read Name
        2. Start:End
        3. Sequence without error
        4. Sequence with error
        5. Substitution coordinates of read seperated by ':'
        6. No. of total errors introdued in read
We can crosscheck the probability of error introduced from this data.

--------
# BWA Alignment :
(https://icb.med.cornell.edu/wiki/index.php/Elementolab/BWA_tutorial)
Indexing : `bwa index -p hg38idx -a bwtsw GRCh38_chromosome17.fa.gz`
Alignment : `bwa aln -t 4 hg38idx reads.fastq.gz > alignment.bwa`
BWA - SAM : `bwa samse hg38idx alignment.bwa reads.fastq.gz > alignment.sam`

Samtools
---
SAM - BAM : `samtools view -bT GRCh38_chromosome17.fa.gz alignment.sam > alignment.bam`
Sorting : `samtools sort alignment.bam alignment.sorted`
BAM - TXT `samtools view alignment.sorted.bam > alignment.sorted.txt`
---------
# Error-rate calculation
(http://fulcrumgenomics.github.io/fgbio/tools/latest/ErrorRateByReadPosition.html)
To get Number of Mapped and Unmapped reads:
`$ samtools index alignment.sorted.bam`
`$ samtools idxstats alignment.sorted.bam`
```sh
17      83257441        99192   0
*       0       0       808
```

Calculate error rate:
(reads mapped on genome position other than where it originated from)
-------------------------------------------------------------------------------------- x 100 = Error Rate
(Total numner of mapped reads)

Run script *calc_error.py* given with commandline argumetns as fastq(gzipped) and alignment(txt)
`$ calc_error.py reads.fastq.gz alignment.sorted.txt`
output:
```sh
13653 reads mapped on genome position other than where it originated from
99192 reads mapped to genome
808 reads not mapped to genome

14% Error Rate (reads mapped on genome position other than where it originated from)
```
-----
# Tools used and versions

| Tool | Version |
| ------ | ------ |
| Python | 2.7.12 |
| BWA | 0.7.12-r1039 |
| Samtools | 0.1.19-96b5f2294a |

Python Modules used:
---
1. sys
2. os
3. numpy
4. random
5. argparser
6. gzip
-----
