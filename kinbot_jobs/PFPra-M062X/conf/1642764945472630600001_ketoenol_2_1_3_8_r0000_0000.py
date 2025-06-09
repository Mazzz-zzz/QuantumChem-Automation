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
            positions=[[np.float64(0.938366), np.float64(0.277931), np.float64(0.257913)], [np.float64(0.197708), np.float64(-0.380888), np.float64(-0.472544)], [np.float64(1.48009), np.float64(1.457475), np.float64(-0.278292)], [np.float64(1.074551), np.float64(2.166576), np.float64(-1.570307)], [np.float64(0.746886), np.float64(3.418416), np.float64(-1.228211)], [np.float64(2.119838), np.float64(2.222497), np.float64(-2.377255)], [np.float64(0.058124), np.float64(1.616821), np.float64(-2.180056)], [np.float64(1.679774), np.float64(-0.747488), np.float64(-1.611598)], [np.float64(2.42017), np.float64(2.074369), np.float64(0.342148)], [np.float64(1.441084), np.float64(-0.127955), np.float64(1.427003)], [np.float64(1.160705), np.float64(-1.040268), np.float64(1.574872)]])

kwargs = {'method': 'am1', 'basis': '', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1642764945472630600001_ketoenol_2_1_3_8_r0000_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None'}
mol.calc = Gaussian(**kwargs)
if 'Gaussian' == 'Gaussian':
    mol.get_potential_energy()
    mol.calc = Gaussian(**kwargs)

const = Constraints(mol)
fix_these = [[idx - 1 for idx in fix] for fix in [[1, 2], [1, 3], [1, 10], [2, 8], [3, 4], [3, 8], [3, 9], [4, 5], [4, 6], [4, 7], [10, 11]]]
for fix in fix_these:
    if len(fix) == 2:
        const.fix_bond(fix)
    elif len(fix) == 4:
        const.fix_dihedral(fix)
    else:
        raise ValueError(f'Unexpected length of fix: {fix}.')

for c in [[np.int64(3), np.int64(1), np.int64(2), np.int64(8), np.float64(-44.93833209895667)]]:
    const.fix_dihedral((c[0]-1, c[1]-1, c[2]-1, c[3]-1), target=c[4])

if os.path.isfile('conf/1642764945472630600001_ketoenol_2_1_3_8_r0000_0000_sella.log'):
    os.remove('conf/1642764945472630600001_ketoenol_2_1_3_8_r0000_0000_sella.log')

sella_kwargs = {}
opt = Sella(mol, 
            order=0, 
            constraints=const,
            trajectory='conf/1642764945472630600001_ketoenol_2_1_3_8_r0000_0000.traj', 
            logfile='conf/1642764945472630600001_ketoenol_2_1_3_8_r0000_0000_sella.log',
            **sella_kwargs,
            )

try:
    mol.calc.label = 'conf/1642764945472630600001_ketoenol_2_1_3_8_r0000_0000'
    opt.run(fmax=1e-4, steps=100)
    e = mol.get_potential_energy()
    db.write(mol, name='conf/1642764945472630600001_ketoenol_2_1_3_8_r0000_0000', 
             data={'energy': e, 'status': 'normal'})
except (RuntimeError, ValueError):
    data = {'status': 'error'}
    db.write(mol, name='conf/1642764945472630600001_ketoenol_2_1_3_8_r0000_0000', data=data)
with open('conf/1642764945472630600001_ketoenol_2_1_3_8_r0000_0000.log', 'a') as f:
    f.write('done\n')
