#!/usr/bin/env python
import os
import sys
import re
import eyed3


def main():

    print('yep, NEW Alt running')
    dir = os.getcwd() if len(sys.argv) == 1 else sys.argv[1] 
    os.chdir(dir)
    filenames_in_dir = os.listdir(dir)

    mpr_search_expr = re.compile('.mp3')


    # they should be sorted in the order provided by system, 
    # but some middle elements ended up in the end
    filenames_in_dir.sort()

    currNumber = 0;
    for filename in filenames_in_dir:
        # ignore non-mp3 files
        if mpr_search_expr.search(filename):
            #change title to number
            audiofile = eyed3.load(filename)
            audiofile.tag.title = get_valid_name_from_index(currNumber)
            audiofile.tag.save()

            #change name to number
            if os.path.exists(get_valid_name_from_index(currNumber)): 
                print( '   ' + get_valid_name_from_index(currNumber) + \
                 'already existed! iteration is on file ' + filename)
            os.rename(filename, get_valid_name_from_index(currNumber))
            currNumber += 1







def get_valid_name_from_index(index):
    '''index must be 0-based, return value is >=1'''
    # no book can ever have 100 chunks, COME ON
    valid_name = str(index + 1) + '.mp3'

    if index + 1 < 10 :
        valid_name = '0' + valid_name

    return valid_name


if __name__ == '__main__':
    main()
