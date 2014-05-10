#!/usr/bin/python
#-*- coding:utf-8 -*-
import os
from subprocess import call

working_dir = '/share/Public/cmiao/ahrd/run'
query_dir = '/share/Public/cmiao/ahrd/run/proteins'
database = [
    '/share/Public/cmiao/ahrd/run/database_swissprot/uniprot_sprot.fasta',
    '/share/Public/cmiao/ahrd/run/database_tair/TAIR10_pep_20101214',
    '/share/Public/cmiao/ahrd/run/database_trembl/uniprot_trembl_plants.fa'
    ]
blastresult_dirs = [
    '/share/Public/cmiao/ahrd/run/blast_result_swissprot',
    '/share/Public/cmiao/ahrd/run/blast_result_tair',
    '/share/Public/cmiao/ahrd/run/blast_result_trembl'
    ]
part_of_blastresult = ['swissprot', 'tair', 'trembl']
ahrd_jar = '/share/Public/cmiao/ahrd/AHRD/dist/ahrd.jar'

def walkdir(dirname):
    '''Walk the directory you pointed and \
save the filenames in this directory to a list.'''
    ls = os.listdir(dirname)
    file_names = []
    for i in ls:
        j = os.path.join(dirname, i)
        file_names.append(j)
    return file_names

def run_blast_file(ls):
    '''ls is query sequence list in which filename is abs path.'''
    f0 = open('blast_commands.txt', 'w')
    for i in ls:
        j = i.split('/')[-1]
        for d, o, p in zip(database, blastresult_dirs, part_of_blastresult):
            f0.write('blastall -p blastp -i %s -d %s -m 0 -e 0.0001 -v 200 \
-b 200 -o %s/%s.%s.pairwise\n'%(i, d, o, j, p))
    f0.close()

def gen_yml(ls):
    '''ls is query sequence list in which filename is abs path.'''
    for i in ls:
        j = i.split('/')[-1]
        f0 = open(working_dir + '/' + j + '.yml', 'w')
        sp_file = '/share/Public/cmiao/ahrd/run/blast_result_swissprot/' + \
j + '.swissprot.pairwise'
        tair_file = '/share/Public/cmiao/ahrd/run/blast_result_tair/' + \
j + '.tair.pairwise'
        tre_file = '/share/Public/cmiao/ahrd/run/blast_result_trembl/' + \
j + '.trembl.pairwise'
        result = '/share/Public/cmiao/ahrd/run/results/' + j + '.csv'
        f0.write('proteins_fasta: ' + i + '\nblast_dbs:\n  swissprot:\n    \
weight: 100\n    file: ' + sp_file + '\n    blacklist: /share/Public/cmiao/\
ahrd/run/blacklist_descline.txt\n    filter: /share/Public/cmiao/ahrd/run/\
filter_descline_sprot.txt\n    token_blacklist: /share/Public/cmiao/ahrd/\
run/blacklist_token.txt\n    description_score_bit_score_weight: 0.2\n\n  \
tair:\n    weight: 50\n    file: ' + tair_file + '\n    blacklist: /share/\
Public/cmiao/ahrd/run/blacklist_descline.txt\n    filter: /share/Public/\
cmiao/ahrd/run/filter_descline_tair.txt\n    token_blacklist: /share/Public/\
cmiao/ahrd/run/blacklist_token.txt\n    description_score_bit_score_weight: \
0.4\n\n  trembl:\n    weight: 10\n    file: ' + tre_file + '\n    \
blacklist: /share/Public/cmiao/ahrd/run/blacklist_descline.txt\n    \
filter: /share/Public/cmiao/ahrd/run/filter_descline_trembl.txt\n    \
token_blacklist: /share/Public/cmiao/ahrd/run/blacklist_token.txt\n    \
description_score_bit_score_weight: 0.4\n\n\
token_score_bit_score_weight: 0.5\ntoken_score_database_score_weight: \
0.3\ntoken_score_overlap_score_weight: \
0.2\ndescription_score_relative_description_frequency_weight: \
0.6\noutput: ' + result + '\n')
        f0.close()

def run_ahrd_file(ls):
    f0 = open('ahrd_commands.txt', 'w')
    for i in ls:
        j = i.split('/')[-1] + '.yml'
        f0.write('java -Xmx2g -jar %s %s/%s\n'%(ahrd_jar, working_dir, j))
    f0.close()

if __name__ == '__main__':
    file_names = walkdir(query_dir)
    print 'Generating command file of blast...'
    run_blast_file(file_names)
    print 'Running blast...'
    call('parallel < blast_commands.txt', shell = True)
    print 'Generating yml files ...'
    gen_yml(file_names)
    print 'Generating command file of ahrd...'
    run_ahrd_file(file_names)
    print 'Runing ahrd now...'
    call('parallel < ahrd_commands.txt', shell = True)
    print 'Run over!!! \nCheck your results in \
/share/Public/cmiao/ahrd/run/results'
