#!/usr/lib/python
#-*-coding:utf-8-*-
from optparse import OptionParser

msg_usage = 'usage: %prog [-F] fastafile [-S] sequencename [-I] posinterva [-O]\
 outputfile'
descr ='''This script is used to fetch a part of sequence from a fasta file.
'''
optparser = OptionParser(usage = msg_usage, description = descr)
optparser.add_option('-F', '--fastafile', dest = 'fafile',
                     help = 'input the fasta file name.')
optparser.add_option('-S', '--sequencename', dest = 'seqname',
                     help = 'your seq name?')
optparser.add_option('-I', '--posinterva', dest = 'seqiv',
                     help = 'choos the interval, e.g. 100-200')
optparser.add_option('-O', '--outputfile', dest = 'output',
                     help = 'output file name.')
options, args = optparser.parse_args()

def fetch_fa(fafile, chr, pos_iv, output):
    st = int(pos_iv.split('-')[0])-1
    ed = int(pos_iv.split('-')[1])
    f0 = open(fafile, 'r')
    new1list = []
    for i in f0:
        if i.startswith('>'):
            new1list.append(i)
        else:
            j = i.strip()  #remove /n
            if j:          #remove space lines
                new1list.append(j)
    f0.close()
    new2list = []
    for i in ''.join(new1list).split('\n'):
        j = i.split('>')
        for k in j:
            if k:
                new2list.append(k)
    NS = {}  # name:sequence
    length = len(new2list)
    for i in range(0, length, 2):
        NS[new2list[i]] = new2list[i+1]
    f1 = open(output, 'w')
    print chr
    print pos_iv
    f1.write('>%s.%s\n'%(chr, pos_iv))
    obseq = NS[chr][st:ed]
    f1.write(obseq)
    f1.close()

if __name__ == '__main__':
    f = options.fafile
    s = options.seqname
    i = options.seqiv
    o = options.output
    fetch_fa(f, s, i, o)



