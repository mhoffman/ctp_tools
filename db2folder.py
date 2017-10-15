#!/usr/bin/env python

import os
import sys


import ase
import ase.io
import ase.db

import errno    
import os


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def main(db_filename, folder_name):
    db = ase.db.connect(db_filename)

    mkdir_p(folder_name)
    for row in db.select():
        atoms = row.toatoms()
        dft_code = row.key_value_pairs['dft_code']
        dft_functional = row.key_value_pairs['dft_functional']
        reaction = row.key_value_pairs['reaction']
        substrate = row.key_value_pairs['substrate']
        facet = row.key_value_pairs['facet'].strip('()')
        adsorbate = row.key_value_pairs['adsorbate']

        out_dirname = "{folder_name}/{dft_code}/{dft_functional}/{reaction}/{substrate}/{facet}".format(**locals())
        out_dirname = out_dirname.replace('/None', '')
        print(out_dirname)
        out_trajname = "{out_dirname}/{adsorbate}.traj".format(**locals())

        mkdir_p(out_dirname)
        ase.io.write(out_trajname, atoms)




if __name__ == '__main__':
    import optparse

    parser = optparse.OptionParser()
    options, args = parser.parse_args()
    if len(args) < 2:
        raise UserWarning('Folder name as input argument expected and db-filename expected.')

    db_filename = args[0]
    folder_name = args[1]
    main(db_filename, folder_name)