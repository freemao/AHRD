#!/usr/bin/python
from optparse import OptionParser

msg_usage = 'usage: %prog [-F] fastafile [-N] seqs per splited file'
descr ='''cause the blast and AHRD limitation of fasta file size
and if your file too large to run blast you'd better to split it
to smaller size this script is created for spliting the fasta file
 '''
optparser = OptionParser(usage = msg_usage, description = descr)
optparser.add_option('-F', '--fastafile', dest = 'fafile',
                      help = 'input the fasta file name.')
optparser.add_option('-N', '--number', dest = 'seqsperfile',type = 'int',
                      help = 'how many sequences per file.')
options, args = optparser.parse_args()

def fa_split(file,n):
    f0=open(file,'r')
    fa=f0.read()
    f1=fa.split('>')
    f1.remove('')
    lens=len(f1)
    s=1
    a=0
    while a+n<=lens-1:
        f2=open(str(s)+'-'+str(a+1)+'--'+str(a+n)+'.fasta','a')
        list1=f1[a:a+n]
        for j in list1:
            f2.write('>'+j)
        f2.close()
        a=a+n
        s=s+1
    else :
        list2=f1[a:]
        f3=open(str(s)+'-'+str(a+1)+'--.fasta','a')
        for k in list2:
            f3.write('>'+k)
        f3.close()
    f0.close()

if __name__=='__main__':
    f = options.fafile
    n = options.seqsperfile
    print('running...')
    fa_split(f, n)
    print ('OK!!! RUN OVER.')
