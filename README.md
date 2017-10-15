### ctp tools

A small collection of tools in and around catapp database project.

So far we have

 -  make_folders_template.py
    - Generate empty folder structure for storing *.traj files organized for catapp input
 -  copy_traj_folders.py
    -  sample script to copy directory of old QE log files into these empty folder as *.traj
      files
 -  folder2db.py
    - turn directory in ase-db representation (without considering metadata)
 -  db2folder.py
    - turn ase-db file back into directory structure
