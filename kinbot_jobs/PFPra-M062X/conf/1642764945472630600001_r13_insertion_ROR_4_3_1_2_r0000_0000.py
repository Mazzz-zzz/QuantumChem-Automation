import os
import sys
import shutil

import numpy as np
from ase import Atoms
from ase.db import connect
from sella import Sella, Constraints

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot.stationary_pt import StationaryPoint


db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
mol = Atoms(symbols=[np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')], 
            positions=[[np.float64(2.177623), np.float64(1.054802), np.float64(-0.036435)], [np.float64(1.217239), np.float64(1.649573), np.float64(0.498422)], [np.float64(1.939343), np.float64(-0.335976), np.float64(-0.346699)], [np.float64(-0.210889), np.float64(0.510255), np.float64(0.140945)], [np.float64(-0.486276), np.float64(-0.747464), np.float64(0.37218)], [np.float64(-0.928742), np.float64(1.193445), np.float64(1.00834)], [np.float64(-0.508877), np.float64(0.891484), np.float64(-1.066436)], [np.float64(2.81797), np.float64(-0.867327), np.float64(-1.210822)], [np.float64(1.931625), np.float64(-1.114779), np.float64(0.761609)], [np.float64(3.254442), np.float64(1.69063), np.float64(-0.411311)], [np.float64(3.124968), np.float64(2.645797), np.float64(-0.323818)]])

kwargs = {'method': 'am1', 'basis': '', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1642764945472630600001_r13_insertion_ROR_4_3_1_2_r0000_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None'}
mol.calc = Gaussian(**kwargs)
if 'Gaussian' == 'Gaussian':
    mol.get_potential_energy()
    mol.calc = Gaussian(**kwargs)

const = Constraints(mol)
fix_these = [[idx - 1 for idx in fix] for fix in [[1, 2], [1, 3], [1, 10], [2, 4], [3, 4], [3, 8], [3, 9], [4, 5], [4, 6], [4, 7], [10, 11]]]
for fix in fix_these:
    if len(fix) == 2:
        const.fix_bond(fix)
    elif len(fix) == 4:
        const.fix_dihedral(fix)
    else:
        raise ValueError(f'Unexpected length of fix: {fix}.')

for c in [[np.int64(2), np.int64(4), np.int64(3), np.int64(1), np.float64(-12.059537571693324)]]:
    const.fix_dihedral((c[0]-1, c[1]-1, c[2]-1, c[3]-1), target=c[4])

if os.path.isfile('conf/1642764945472630600001_r13_insertion_ROR_4_3_1_2_r0000_0000_sella.log'):
    os.remove('conf/1642764945472630600001_r13_insertion_ROR_4_3_1_2_r0000_0000_sella.log')

sella_kwargs = {}
opt = Sella(mol, 
            order=0, 
            constraints=const,
            trajectory='conf/1642764945472630600001_r13_insertion_ROR_4_3_1_2_r0000_0000.traj', 
            logfile='conf/1642764945472630600001_r13_insertion_ROR_4_3_1_2_r0000_0000_sella.log',
            **sella_kwargs,
            )

try:
    mol.calc.label = 'conf/1642764945472630600001_r13_insertion_ROR_4_3_1_2_r0000_0000'
    opt.run(fmax=1e-4, steps=100)
    e = mol.get_potential_energy()
    db.write(mol, name='conf/1642764945472630600001_r13_insertion_ROR_4_3_1_2_r0000_0000', 
             data={'energy': e, 'status': 'normal'})
except (RuntimeError, ValueError):
    data = {'status': 'error'}
    db.write(mol, name='conf/1642764945472630600001_r13_insertion_ROR_4_3_1_2_r0000_0000', data=data)
with open('conf/1642764945472630600001_r13_insertion_ROR_4_3_1_2_r0000_0000.log', 'a') as f:
    f.write('done\n')
