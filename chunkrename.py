#!/usr/bin/env python
import os
import sys
import re
import eyed3
import string

def main():

    dir = os.getcwd() if len(sys.argv) == 1 else sys.argv[1] 
    os.chdir(dir)
    filenames_in_dir = os.listdir(dir)

    minutes_extract = re.compile('\_(\d*).*\_')
    rename_re = re.compile('\_.*')
    mpr_search_expr = re.compile('.mp3')


    for filename in filenames_in_dir:
        if not mpr_search_expr.search(filename): 
            continue

        match = minutes_extract.search(filename)
        if(match):
            minutes = match.group(1)
            os.rename(filename, rename_re.sub(string=filename, repl= (" " + minutes + '.mp3')))

    





if __name__ == '__main__':
    main()