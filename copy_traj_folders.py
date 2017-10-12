#!/usr/bin/env python

import os
import shutil

import ase.io
import ase.io.trajectory
import espresso.io

adsorbates = ['O', 'H', 'C', 'N', 'CO', 'NO', 'CH', 'S', 'CO',]
surfaces = ['Pt', 'Pd', 'Rh', 'Ir', 'Ag', 'Cu']
facets = ['111-(1x1)', '111-(2x2)', '111-(4x4)']

src_dir = '/nfs/slac/g/suncatfs/maxjh/calculations/learn_quantum_espresso/DOS/with_adsorbates'


for surface in surfaces:
    for adsorbate in adsorbates:
        reaction = '{adsorbate}star__{adsorbate}gas_star'.format(**locals())
        gas_traj_file = '{src_dir}/../../molecules_spin/gas_phase_{adsorbate}_final_geom.traj'.format(**locals())
        gas_target_file = 'hoffmann_framework_2016/Quantum ESPRESSO/BEEF-vdW/{reaction}/{adsorbate}_gas.traj'.format(**locals())
        gas_energy = espresso.io.read_energies('{src_dir}/../../molecules_spin/gas_phase_{adsorbate}/log'.format(**locals()))
        
        shutil.copy(gas_traj_file, gas_target_file)

        ase.io.trajectory.convert(gas_target_file)
        traj1 = ase.io.trajectory.Trajectory(gas_target_file)
        atoms1 = ase.io.trajectory.read_atoms(traj1.backend)
        traj2 = ase.io.Trajectory(gas_target_file, 'w')
        traj2.write(atoms1, energy=gas_energy)

        for facet in facets:
            x, y = facet.replace('(', '').replace(')', '').split('-')[1].split('x')

            traj_file = '{src_dir}/adsorbate_{surface}111_{x}_{y}_{adsorbate}_fcc_final_geom.traj'.format(**locals())
            clean_traj_file = '{src_dir}/adsorbate_{surface}111_1_1_clean_ontop_final_geom.traj'.format(**locals())
            target_dir = 'hoffmann_framework_2016/Quantum ESPRESSO/BEEF-vdW/{reaction}/{surface}/{facet}'.format(**locals())
            clean_target_filename = '{target_dir}/clean-(1x1).traj'.format(**locals())
            adsorbate_target_filename = '{target_dir}/{adsorbate}.traj'.format(**locals())

            adsorbed_energy = espresso.io.read_energies('{src_dir}/adsorbate_{surface}111_{x}_{y}_{adsorbate}_fcc/log'.format(**locals()))
            clean_energy = espresso.io.read_energies('{src_dir}/adsorbate_{surface}111_1_1_clean_ontop/log'.format(**locals()))


            if os.path.exists(traj_file):
                print(traj_file)
                #print(adsorbate_target_filename)
                # first just copy
                shutil.copy(traj_file, adsorbate_target_filename)
                shutil.copy(clean_traj_file, clean_target_filename)

                # then convert to new format and add energy
                try:
                    ase.io.trajectory.convert(adsorbate_target_filename)
                    traj1 = ase.io.trajectory.Trajectory(adsorbate_target_filename)
                    atoms1 = ase.io.trajectory.read_atoms(traj1.backend)
                    traj2 = ase.io.Trajectory(adsorbate_target_filename, 'w')
                    traj2.write(atoms1, energy=adsorbed_energy)

                    ase.io.trajectory.convert(clean_target_filename)
                    traj1 = ase.io.trajectory.Trajectory(clean_target_filename)
                    atoms1 = ase.io.trajectory.read_atoms(traj1.backend)
                    traj2 = ase.io.Trajectory(clean_target_filename, 'w')
                    traj2.write(atoms1, energy=clean_energy)
                except IOError:
                    print("Skipping {traj_file}".format(**locals()))

