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
            positions=[[np.float64(1.349557), np.float64(0.149231), np.float64(-0.367695)], [np.float64(1.995199), np.float64(-0.851591), np.float64(-0.678598)], [np.float64(-0.006493), np.float64(-0.205456), np.float64(0.25563)], [np.float64(-0.650103), np.float64(0.389253), np.float64(1.531983)], [np.float64(-1.851967), np.float64(-0.124653), np.float64(1.727879)], [np.float64(0.134476), np.float64(0.071106), np.float64(2.546037)], [np.float64(-0.742019), np.float64(1.692037), np.float64(1.406186)], [np.float64(0.619313), np.float64(0.857527), np.float64(-1.464032)], [np.float64(-0.662123), np.float64(-1.139548), np.float64(-0.2485)], [np.float64(1.900454), np.float64(1.164825), np.float64(0.38049)], [np.float64(2.843203), np.float64(0.968674), np.float64(0.422713)]])

kwargs = {'method': 'am1', 'basis': '', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1642764945472630600001_r12_insertion_R_1_3_8_r0000_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None'}
mol.calc = Gaussian(**kwargs)
if 'Gaussian' == 'Gaussian':
    mol.get_potential_energy()
    mol.calc = Gaussian(**kwargs)

const = Constraints(mol)
fix_these = [[idx - 1 for idx in fix] for fix in [[1, 2], [1, 3], [1, 8], [1, 10], [2, 3], [3, 4], [3, 8], [3, 9], [4, 5], [4, 6], [4, 7], [10, 11]]]
for fix in fix_these:
    if len(fix) == 2:
        const.fix_bond(fix)
    elif len(fix) == 4:
        const.fix_dihedral(fix)
    else:
        raise ValueError(f'Unexpected length of fix: {fix}.')

for c in [[np.int64(3), np.int64(8), np.int64(1), np.int64(2), np.float64(-71.86190174348974)]]:
    const.fix_dihedral((c[0]-1, c[1]-1, c[2]-1, c[3]-1), target=c[4])

if os.path.isfile('conf/1642764945472630600001_r12_insertion_R_1_3_8_r0000_0000_sella.log'):
    os.remove('conf/1642764945472630600001_r12_insertion_R_1_3_8_r0000_0000_sella.log')

sella_kwargs = {}
opt = Sella(mol, 
            order=0, 
            constraints=const,
            trajectory='conf/1642764945472630600001_r12_insertion_R_1_3_8_r0000_0000.traj', 
            logfile='conf/1642764945472630600001_r12_insertion_R_1_3_8_r0000_0000_sella.log',
            **sella_kwargs,
            )

try:
    mol.calc.label = 'conf/1642764945472630600001_r12_insertion_R_1_3_8_r0000_0000'
    opt.run(fmax=1e-4, steps=100)
    e = mol.get_potential_energy()
    db.write(mol, name='conf/1642764945472630600001_r12_insertion_R_1_3_8_r0000_0000', 
             data={'energy': e, 'status': 'normal'})
except (RuntimeError, ValueError):
    data = {'status': 'error'}
    db.write(mol, name='conf/1642764945472630600001_r12_insertion_R_1_3_8_r0000_0000', data=data)
with open('conf/1642764945472630600001_r12_insertion_R_1_3_8_r0000_0000.log', 'a') as f:
    f.write('done\n')
