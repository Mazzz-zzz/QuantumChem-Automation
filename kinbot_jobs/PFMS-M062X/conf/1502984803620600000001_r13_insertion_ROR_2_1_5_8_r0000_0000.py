import os
import sys
import shutil

import numpy as np
from ase import Atoms
from ase.db import connect
from sella import Sella, Constraints

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot.stationary_pt import StationaryPoint


db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFMS-M062X/kinbot.db')
mol = Atoms(symbols=[np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('H')], 
            positions=[[np.float64(1.589658), np.float64(0.083565), np.float64(-0.081593)], [np.float64(-0.475985), np.float64(0.560446), np.float64(0.086774)], [np.float64(1.618328), np.float64(-0.674739), np.float64(0.921)], [np.float64(1.519704), np.float64(-0.551001), np.float64(-1.161536)], [np.float64(2.08696), np.float64(1.962006), np.float64(0.025258)], [np.float64(3.315424), np.float64(1.796993), np.float64(0.722097)], [np.float64(2.09781), np.float64(2.290736), np.float64(-1.354794)], [np.float64(0.959781), np.float64(2.429146), np.float64(0.801738)], [np.float64(-0.231334), np.float64(1.430541), np.float64(0.418634)]])

kwargs = {'method': 'am1', 'basis': '', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1502984803620600000001_r13_insertion_ROR_2_1_5_8_r0000_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None'}
mol.calc = Gaussian(**kwargs)
if 'Gaussian' == 'Gaussian':
    mol.get_potential_energy()
    mol.calc = Gaussian(**kwargs)

const = Constraints(mol)
fix_these = [[idx - 1 for idx in fix] for fix in [[1, 2], [1, 3], [1, 4], [1, 5], [2, 9], [5, 6], [5, 7], [5, 8], [8, 9]]]
for fix in fix_these:
    if len(fix) == 2:
        const.fix_bond(fix)
    elif len(fix) == 4:
        const.fix_dihedral(fix)
    else:
        raise ValueError(f'Unexpected length of fix: {fix}.')

for c in [[np.int64(9), np.int64(8), np.int64(5), np.int64(1), np.float64(-24.273971076974)]]:
    const.fix_dihedral((c[0]-1, c[1]-1, c[2]-1, c[3]-1), target=c[4])

if os.path.isfile('conf/1502984803620600000001_r13_insertion_ROR_2_1_5_8_r0000_0000_sella.log'):
    os.remove('conf/1502984803620600000001_r13_insertion_ROR_2_1_5_8_r0000_0000_sella.log')

sella_kwargs = {}
opt = Sella(mol, 
            order=0, 
            constraints=const,
            trajectory='conf/1502984803620600000001_r13_insertion_ROR_2_1_5_8_r0000_0000.traj', 
            logfile='conf/1502984803620600000001_r13_insertion_ROR_2_1_5_8_r0000_0000_sella.log',
            **sella_kwargs,
            )

try:
    mol.calc.label = 'conf/1502984803620600000001_r13_insertion_ROR_2_1_5_8_r0000_0000'
    opt.run(fmax=1e-4, steps=100)
    e = mol.get_potential_energy()
    db.write(mol, name='conf/1502984803620600000001_r13_insertion_ROR_2_1_5_8_r0000_0000', 
             data={'energy': e, 'status': 'normal'})
except (RuntimeError, ValueError):
    data = {'status': 'error'}
    db.write(mol, name='conf/1502984803620600000001_r13_insertion_ROR_2_1_5_8_r0000_0000', data=data)
with open('conf/1502984803620600000001_r13_insertion_ROR_2_1_5_8_r0000_0000.log', 'a') as f:
    f.write('done\n')
