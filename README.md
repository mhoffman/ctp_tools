### ctp tools

A small collection of tools in and around catapp database project.

So far we have

 -  make_folders_template.py
    - Generate empty folder structure for storing .traj files organized for catapp input
 -  copy_traj_folders.py
    -  Sample script to copy directory of old QE log files into these empty folder as .traj
      files
 -  folder2db.py
    - Turn directory in ase-db representation. The data in publication.txt is stored in corresponding `publication_*`
        in each system row.
 -  db2folder.py
    - Turn ase-db file back into directory structure
