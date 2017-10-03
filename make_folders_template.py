#!/usr/bin/python

import os
import sys
import json
sys.path.append('/nfs/slac/g/suncatfs/data_catapp')
from tools import extract_atoms, check_reaction 

"""
Dear all

Use this script to make the right structure for your folders.
Folders will be created automatically when you run the script with python.
Start by copying the script to a folder in your username,
and assign the right information to the variables below.

You can change the parameters and run the script several times if you,
for example, are using different functionals or are doing different reactions
on different surfaces.
"""

username = os.environ['USER']

# ---------publication info------------

title = 'Fancy title'  # work title if not yet published
authors = ['Doe, John', 'Einstein, Albert']  # name required
journal = ''
volume = ''
number = ''
pages = ''
year = '2017'  # year required
publisher = ''

DFT_code = ''  # for example 'Quantum ESPRESSO'
DFT_functional = ''  # For example 'BEEF-vdW'           

#  ---------molecules info-----------

# reactants[i] -> products_A[i] + products_B[i] 

reactants = ['CCH3', 'CH3star']  # Update!
products_A = ['C', 'CH3gas']
products_B = ['CH3', 'star'] 

"""
Include the phase if necessary:

'star' for empty site or adsorbed phase. Only necessary to put 'star' if
gas phase species are also involved.
'gas' if in gas phase

Remember to include the adsorption energy of reaction intermediates, taking
gas phase molecules as references (preferably H20, H2, CH4, CO, NH3).
For example, we can write the desorption of CH2 as:
CH2* -> CH4(g) - H2(g) + *
Here you would have to write 'CH4gas-H2gas' as "products_A" entry.

See example:
reactants = ['CH2star', 'CH3star']
products_A = ['CH4gas-H2gas', 'CH4gas-0.5H2gas']
products_B = ['star', 'star']
"""

# ---------------surface info---------------------

# If complicated structure: use term you would use in publication
surfaces = ['Pt']
facets = ['111']

#  ----------- You're done!------------------------  

# Check reactions
assert len(reactants) == len(products_A) == len(products_B)
for AB, A, B in zip(reactants, products_A, products_B):
    check_reaction(AB, A, B)

# Set up directories
base = '/nfs/slac/g/suncatfs/data_catapp/%s/' % username

if not os.path.exists(base):
    os.mkdir(base)

publication_shortname = '%s_%s_%s' % (authors[0].split(',')[0].lower(),
                                      title.split()[0].lower(), year)

publication_base = base + publication_shortname + '/'

if not os.path.exists(publication_base):
    os.mkdir(publication_base)

# save publication info to publications.txt
publication_dict = {'title': title,
                    'authors': authors,
                    'journal': journal,
                    'volume': volume,
                    'number': number,
                    'pages': pages,
                    'year': year,
                    'publisher': publisher
                    }

pub_txt = publication_base + 'publication.txt'
json.dump(publication_dict, open(pub_txt, 'wb'))

create = []  # list of directories to be made
create.append(publication_base + DFT_code + '/')
create.append(create[-1] + DFT_functional + '/')

base_reactions = create[-1]

for i in range(len(reactants)):
    reaction = '%s_%s_%s' % (reactants[i], products_A[i], products_B[i])
    create.append(base_reactions + reaction + '/')
    base_surfaces = create[-1]
    for surface in surfaces:
        create.append(base_surfaces + surface + '/')
        base_facets = create[-1]        
        for facet in facets:
            create.append(base_facets + facet + '/')

for path in create:
    if not os.path.exists(path):
        os.mkdir(path)

 
