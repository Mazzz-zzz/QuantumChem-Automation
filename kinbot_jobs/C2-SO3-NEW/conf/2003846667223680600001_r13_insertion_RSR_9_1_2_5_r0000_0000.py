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
            positions=[[np.float64(1.780739), np.float64(-0.040251), np.float64(-0.078062)], [np.float64(2.361133), np.float64(1.242847), np.float64(0.065012)], [np.float64(3.122724), np.float64(1.424866), np.float64(1.134949)], [np.float64(2.911031), np.float64(1.732084), np.float64(-1.034211)], [np.float64(0.46657), np.float64(2.476423), np.float64(0.49844)], [np.float64(0.605401), np.float64(2.266214), np.float64(1.915644)], [np.float64(1.069998), np.float64(3.517723), np.float64(-0.289935)], [np.float64(-1.08884), np.float64(2.764074), np.float64(0.20812)], [np.float64(-0.056725), np.float64(0.682809), np.float64(-0.152488)], [np.float64(1.664086), np.float64(-0.620285), np.float64(-1.211363)], [np.float64(1.599962), np.float64(-0.793355), np.float64(0.936442)], [np.float64(-1.613159), np.float64(2.006416), np.float64(0.498735)]])

kwargs = {'method': 'am1', 'basis': '', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_RSR_9_1_2_5_r0000_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None'}
mol.calc = Gaussian(**kwargs)
if 'Gaussian' == 'Gaussian':
    mol.get_potential_energy()
    mol.calc = Gaussian(**kwargs)

const = Constraints(mol)
fix_these = [[idx - 1 for idx in fix] for fix in [[1, 2], [1, 9], [1, 10], [1, 11], [2, 3], [2, 4], [2, 5], [5, 6], [5, 7], [5, 8], [5, 9], [8, 12]]]
for fix in fix_these:
    if len(fix) == 2:
        const.fix_bond(fix)
    elif len(fix) == 4:
        const.fix_dihedral(fix)
    else:
        raise ValueError(f'Unexpected length of fix: {fix}.')

for c in [[np.int64(5), np.int64(9), np.int64(1), np.int64(2), np.float64(-11.79284254628832)]]:
    const.fix_dihedral((c[0]-1, c[1]-1, c[2]-1, c[3]-1), target=c[4])

if os.path.isfile('conf/2003846667223680600001_r13_insertion_RSR_9_1_2_5_r0000_0000_sella.log'):
    os.remove('conf/2003846667223680600001_r13_insertion_RSR_9_1_2_5_r0000_0000_sella.log')

sella_kwargs = {}
opt = Sella(mol, 
            order=0, 
            constraints=const,
            trajectory='conf/2003846667223680600001_r13_insertion_RSR_9_1_2_5_r0000_0000.traj', 
            logfile='conf/2003846667223680600001_r13_insertion_RSR_9_1_2_5_r0000_0000_sella.log',
            **sella_kwargs,
            )

try:
    mol.calc.label = 'conf/2003846667223680600001_r13_insertion_RSR_9_1_2_5_r0000_0000'
    opt.run(fmax=1e-4, steps=100)
    e = mol.get_potential_energy()
    db.write(mol, name='conf/2003846667223680600001_r13_insertion_RSR_9_1_2_5_r0000_0000', 
             data={'energy': e, 'status': 'normal'})
except (RuntimeError, ValueError):
    data = {'status': 'error'}
    db.write(mol, name='conf/2003846667223680600001_r13_insertion_RSR_9_1_2_5_r0000_0000', data=data)
with open('conf/2003846667223680600001_r13_insertion_RSR_9_1_2_5_r0000_0000.log', 'a') as f:
    f.write('done\n')
