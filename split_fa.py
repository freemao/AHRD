#!/usr/bin/python
'''
cause the blast and AHRD limitation of fasta file size
and if your file too large to run blast
you'd better to split it to smaller size
this script is created for spliting the fasta file
'''
def fa_split(file,n,*args):
    '''
    file:which file you wanna tackle
    n:sequence number per splitted file
    '''
    f0=open(file,'r')
    fa=f0.read()
    f1=fa.split('>')
    f1.remove('')
    lens=len(f1)
    s=1
    a=0
    while a+n<=lens-1:
        f2=open(str(s)+','+str(a+1)+'--'+str(a+n)+'.fasta','a')
        list1=f1[a:a+n]
        for j in list1:
            f2.write('>'+j)
        f2.close()
        a=a+n
        s=s+1
    else :
        list2=f1[a:]
        f3=open(str(s)+','+str(a+1)+'--.fasta','a')
        for k in list2:
            f3.write('>'+k)
        f3.close()
    f0.close()
import sys
if __name__=='__main__':
    print('running...')
    fa_split(sys.argv[1],int(sys.argv[2]))
    print ('OK!!! RUN OVER.')
