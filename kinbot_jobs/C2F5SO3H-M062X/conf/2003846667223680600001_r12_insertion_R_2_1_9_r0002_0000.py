import os
import sys
import shutil

import numpy as np
from ase import Atoms
from ase.db import connect
from sella import Sella, Constraints

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot.stationary_pt import StationaryPoint


db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], 
            positions=[[np.float64(-0.639583), np.float64(-1.066889), np.float64(0.58233)], [np.float64(-0.094144), np.float64(0.041475), np.float64(-0.364908)], [np.float64(-0.501269), np.float64(-0.123626), np.float64(-1.603513)], [np.float64(-0.593349), np.float64(1.18854), np.float64(0.091515)], [np.float64(1.695901), np.float64(-0.227328), np.float64(0.028277)], [np.float64(1.482476), np.float64(-0.836928), np.float64(1.336071)], [np.float64(2.767535), np.float64(-0.362488), np.float64(-0.901306)], [np.float64(1.913839), np.float64(1.313977), np.float64(0.487658)], [np.float64(0.967776), np.float64(-1.860806), np.float64(-0.670805)], [np.float64(-0.97475), np.float64(-0.748354), np.float64(1.75331)], [np.float64(-1.202252), np.float64(-2.116487), np.float64(0.205942)], [np.float64(2.625751), np.float64(1.678503), np.float64(-0.050374)]])

kwargs = {'method': 'am1', 'basis': '', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r12_insertion_R_2_1_9_r0002_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None'}
mol.calc = Gaussian(**kwargs)
if 'Gaussian' == 'Gaussian':
    mol.get_potential_energy()
    mol.calc = Gaussian(**kwargs)

const = Constraints(mol)
fix_these = [[idx - 1 for idx in fix] for fix in [[1, 2], [1, 6], [1, 9], [1, 10], [1, 11], [2, 3], [2, 4], [2, 5], [5, 6], [5, 7], [5, 8], [5, 9], [8, 12]]]
for fix in fix_these:
    if len(fix) == 2:
        const.fix_bond(fix)
    elif len(fix) == 4:
        const.fix_dihedral(fix)
    else:
        raise ValueError(f'Unexpected length of fix: {fix}.')

for c in [[np.int64(1), np.int64(6), np.int64(5), np.int64(9), np.float64(-51.56983658540489)]]:
    const.fix_dihedral((c[0]-1, c[1]-1, c[2]-1, c[3]-1), target=c[4])

if os.path.isfile('conf/2003846667223680600001_r12_insertion_R_2_1_9_r0002_0000_sella.log'):
    os.remove('conf/2003846667223680600001_r12_insertion_R_2_1_9_r0002_0000_sella.log')

sella_kwargs = {}
opt = Sella(mol, 
            order=0, 
            constraints=const,
            trajectory='conf/2003846667223680600001_r12_insertion_R_2_1_9_r0002_0000.traj', 
            logfile='conf/2003846667223680600001_r12_insertion_R_2_1_9_r0002_0000_sella.log',
            **sella_kwargs,
            )

try:
    mol.calc.label = 'conf/2003846667223680600001_r12_insertion_R_2_1_9_r0002_0000'
    opt.run(fmax=1e-4, steps=100)
    e = mol.get_potential_energy()
    db.write(mol, name='conf/2003846667223680600001_r12_insertion_R_2_1_9_r0002_0000', 
             data={'energy': e, 'status': 'normal'})
except (RuntimeError, ValueError):
    data = {'status': 'error'}
    db.write(mol, name='conf/2003846667223680600001_r12_insertion_R_2_1_9_r0002_0000', data=data)
with open('conf/2003846667223680600001_r12_insertion_R_2_1_9_r0002_0000.log', 'a') as f:
    f.write('done\n')
