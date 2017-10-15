#!/usr/bin/env python

# builtin imports
import os
import os.path
import sys

# other imports
import ase
import ase.db
import ase.io


def store_node(db_filename, dirname, names):
    db = ase.db.connect(db_filename)
    for name in names:
        if name.endswith('.traj'):
            sys.stdout.write('.')
            dsplit = dirname.split('/')
            if len(dsplit) == 6: #adsorbed structure
                #print(len(dsplit))
                publication, dft_code, dft_functional, reaction, substrate, facet = dsplit
            elif len(dsplit) == 4: # gas phase molecule
                publication, dft_code, dft_functional, reaction = dsplit
                substrate, facet = 'None', 'None'
                # have to use string because ase.db does not accept None
            else:
                continue

            if not facet == 'None':
                facet = '({facet})'.format(**locals())

            atoms = ase.io.read(os.path.join(dirname, name))
            db.write(atoms,
                    publication=publication,
                    dft_code=dft_code,
                    dft_functional=dft_functional,
                    reaction=reaction,
                    substrate=substrate,
                    facet=facet,
                    )


if __name__ == '__main__':
    import optparse

    parser = optparse.OptionParser()
    options, args = parser.parse_args()
    if len(args) < 2:
        raise UserWarning('Folder name as input argument expected and db-filename expected.')

    folder_name = args[0]
    db_filename = args[1]

    os.path.walk(folder_name, store_node, db_filename)
    sys.stdout.write(' Done!\n')
