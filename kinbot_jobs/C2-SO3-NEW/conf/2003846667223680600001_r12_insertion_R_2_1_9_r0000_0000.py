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
            positions=[[np.float64(-0.657138), np.float64(0.11354), np.float64(1.460719)], [np.float64(-0.240013), np.float64(0.156737), np.float64(-0.041892)], [np.float64(-0.641271), np.float64(-0.860341), np.float64(-0.761261)], [np.float64(-0.72759), np.float64(1.272293), np.float64(-0.5851)], [np.float64(1.57807), np.float64(0.301842), np.float64(0.372728)], [np.float64(1.304107), np.float64(0.773386), np.float64(1.759009)], [np.float64(2.654114), np.float64(-0.499062), np.float64(-0.138206)], [np.float64(1.823859), np.float64(1.735118), np.float64(-0.368358)], [np.float64(0.763925), np.float64(-1.42101), np.float64(1.162086)], [np.float64(-1.036346), np.float64(1.228384), np.float64(1.972878)], [np.float64(-1.307423), np.float64(-0.831776), np.float64(1.994929)], [np.float64(2.536128), np.float64(1.628915), np.float64(-1.009239)]])

kwargs = {'method': 'am1', 'basis': '', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r12_insertion_R_2_1_9_r0000_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None'}
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

for c in [[np.int64(2), np.int64(5), np.int64(6), np.int64(1), np.float64(-16.459396334746174)]]:
    const.fix_dihedral((c[0]-1, c[1]-1, c[2]-1, c[3]-1), target=c[4])

if os.path.isfile('conf/2003846667223680600001_r12_insertion_R_2_1_9_r0000_0000_sella.log'):
    os.remove('conf/2003846667223680600001_r12_insertion_R_2_1_9_r0000_0000_sella.log')

sella_kwargs = {}
opt = Sella(mol, 
            order=0, 
            constraints=const,
            trajectory='conf/2003846667223680600001_r12_insertion_R_2_1_9_r0000_0000.traj', 
            logfile='conf/2003846667223680600001_r12_insertion_R_2_1_9_r0000_0000_sella.log',
            **sella_kwargs,
            )

try:
    mol.calc.label = 'conf/2003846667223680600001_r12_insertion_R_2_1_9_r0000_0000'
    opt.run(fmax=1e-4, steps=100)
    e = mol.get_potential_energy()
    db.write(mol, name='conf/2003846667223680600001_r12_insertion_R_2_1_9_r0000_0000', 
             data={'energy': e, 'status': 'normal'})
except (RuntimeError, ValueError):
    data = {'status': 'error'}
    db.write(mol, name='conf/2003846667223680600001_r12_insertion_R_2_1_9_r0000_0000', data=data)
with open('conf/2003846667223680600001_r12_insertion_R_2_1_9_r0000_0000.log', 'a') as f:
    f.write('done\n')
