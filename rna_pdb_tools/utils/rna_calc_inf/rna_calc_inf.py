#!/usr/bin/python

"""
A tool to calc inf_all, inf_stack, inf_WC, inf_nWC, SNS_WC, PPV_WC, SNS_nWC, PPV_nWC between two structures.

ClaRNA_play required!
https://gitlab.genesilico.pl/RNA/ClaRNA_play (internal GS gitlab server)

"""

import argparse
import sys
import os
import subprocess
import re

def clarna_run(fn, force):
    """Run ClaRNA run"""
    fn_out = fn + '.outCR'
    if os.path.isfile(fn_out) and not force:
        pass
    else:
        cmd = 'clarna_run.py -ipdb ' + fn + ' > ' + fn_out
        print cmd
        os.system(cmd)
    return fn_out

def clarna_compare(target_cl_fn,i_cl_fn):
    """Run ClaRNA compare"""
    cmd = 'clarna_compare.py -iref ' + target_cl_fn + ' -ichk ' + i_cl_fn
    o = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    std = o.stdout.read().strip()
    return std
    
def get_parser():
    parser =  argparse.ArgumentParser()#usage="%prog [<options>] <pdb files (test_data/*)>")

    parser.add_argument('-t',"--target_fn",
                           dest="target_fn",
                         default='',
                         help="pdb file")

    parser.add_argument('-f',"--force",
                         dest="force",
                         action="store_true",
                         help="force to run ClaRNA")

    parser.add_argument('-o',"--out_fn",
                         dest="out_fn",
                         default='inf.csv',
                         help="out csv file")

    parser.add_argument('files', help="files", nargs='+')

    return parser
    
if __name__ == '__main__':
    print 'rna_calc_inf'
    print '-' * 80

    parser = get_parser()
    args = parser.parse_args()

    if len(sys.argv) == 1:
        print parser.print_help()
        sys.exit(1)

    input_files = args.files
    target_fn = args.target_fn
    out_fn = args.out_fn
    print 'target, fn, inf_all, inf_stack, inf_WC, inf_nWC, SNS_WC, PPV_WC, SNS_nWC, PPV_nWC'
    target_cl_fn = clarna_run(target_fn, args.force)    
    f = open(out_fn, 'w')
    #t = 'target:' + os.path.basename(target_fn) + ' , rmsd_all\n'
    t = 'target,fn,inf_all, inf_stack, inf_WC, inf_nWC, SNS_WC, PPV_WC, SNS_nWC, PPV_nWC\n'
    f.write(t)
    for i in input_files:
        i_cl_fn = clarna_run(i, args.force)
        scores = clarna_compare(target_cl_fn,i_cl_fn)
        print scores
        f.write(re.sub('\s+', ',', scores) + '\n')
    print 'csv was created! ', out_fn
