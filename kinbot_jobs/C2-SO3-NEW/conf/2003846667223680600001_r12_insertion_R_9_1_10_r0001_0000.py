import os
import sys
import shutil

import numpy as np
from ase import Atoms
from ase.db import connect
from sella import Sella, Constraints

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot.stationary_pt import StationaryPoint


db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], 
            positions=[[np.float64(-1.061763), np.float64(-0.14689), np.float64(1.024145)], [np.float64(-0.426978), np.float64(0.640948), np.float64(0.06014)], [np.float64(-0.568073), np.float64(0.285147), np.float64(-1.200221)], [np.float64(-0.474803), np.float64(1.953604), np.float64(0.240388)], [np.float64(1.847095), np.float64(0.033097), np.float64(0.541032)], [np.float64(2.652575), np.float64(0.68619), np.float64(1.541196)], [np.float64(2.047132), np.float64(-1.201201), np.float64(-0.154817)], [np.float64(1.93613), np.float64(1.129863), np.float64(-0.699098)], [np.float64(-1.448539), np.float64(0.325), np.float64(2.143498)], [np.float64(0.765937), np.float64(-0.744654), np.float64(1.873622)], [np.float64(-1.424654), np.float64(-1.341343), np.float64(0.773447)], [np.float64(2.206364), np.float64(1.978271), np.float64(-0.325035)]])

kwargs = {'method': 'am1', 'basis': '', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r12_insertion_R_9_1_10_r0001_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None'}
mol.calc = Gaussian(**kwargs)
if 'Gaussian' == 'Gaussian':
    mol.get_potential_energy()
    mol.calc = Gaussian(**kwargs)

const = Constraints(mol)
fix_these = [[idx - 1 for idx in fix] for fix in [[1, 2], [1, 9], [1, 10], [1, 11], [2, 3], [2, 4], [2, 5], [5, 6], [5, 7], [5, 8], [5, 10], [8, 12]]]
for fix in fix_these:
    if len(fix) == 2:
        const.fix_bond(fix)
    elif len(fix) == 4:
        const.fix_dihedral(fix)
    else:
        raise ValueError(f'Unexpected length of fix: {fix}.')

for c in [[np.int64(10), np.int64(1), np.int64(2), np.int64(5), np.float64(0.0)]]:
    const.fix_dihedral((c[0]-1, c[1]-1, c[2]-1, c[3]-1), target=c[4])

if os.path.isfile('conf/2003846667223680600001_r12_insertion_R_9_1_10_r0001_0000_sella.log'):
    os.remove('conf/2003846667223680600001_r12_insertion_R_9_1_10_r0001_0000_sella.log')

sella_kwargs = {}
opt = Sella(mol, 
            order=0, 
            constraints=const,
            trajectory='conf/2003846667223680600001_r12_insertion_R_9_1_10_r0001_0000.traj', 
            logfile='conf/2003846667223680600001_r12_insertion_R_9_1_10_r0001_0000_sella.log',
            **sella_kwargs,
            )

try:
    mol.calc.label = 'conf/2003846667223680600001_r12_insertion_R_9_1_10_r0001_0000'
    opt.run(fmax=1e-4, steps=100)
    e = mol.get_potential_energy()
    db.write(mol, name='conf/2003846667223680600001_r12_insertion_R_9_1_10_r0001_0000', 
             data={'energy': e, 'status': 'normal'})
except (RuntimeError, ValueError):
    data = {'status': 'error'}
    db.write(mol, name='conf/2003846667223680600001_r12_insertion_R_9_1_10_r0001_0000', data=data)
with open('conf/2003846667223680600001_r12_insertion_R_9_1_10_r0001_0000.log', 'a') as f:
    f.write('done\n')
