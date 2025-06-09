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
            positions=[[np.float64(2.460871), np.float64(1.156114), np.float64(-0.071532)], [np.float64(2.470743), np.float64(1.823999), np.float64(0.962821)], [np.float64(1.945939), np.float64(-0.147715), np.float64(0.014674)], [np.float64(1.62198), np.float64(-0.94033), np.float64(1.280952)], [np.float64(2.320549), np.float64(-2.079399), np.float64(1.203651)], [np.float64(1.941776), np.float64(-0.324271), np.float64(2.387936)], [np.float64(0.336425), np.float64(-1.247189), np.float64(1.279912)], [np.float64(0.565667), np.float64(1.823621), np.float64(0.957719)], [np.float64(1.707241), np.float64(-0.81767), np.float64(-1.054594)], [np.float64(2.693836), np.float64(1.621973), np.float64(-1.301554)], [np.float64(2.823908), np.float64(2.57715), np.float64(-1.242065)]])

kwargs = {'method': 'am1', 'basis': '', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1642764945472630600001_r13_insertion_ROR_8_3_1_2_r0002_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None'}
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

for c in [[np.int64(1), np.int64(2), np.int64(8), np.int64(3), np.float64(44.94569719851714)]]:
    const.fix_dihedral((c[0]-1, c[1]-1, c[2]-1, c[3]-1), target=c[4])

if os.path.isfile('conf/1642764945472630600001_r13_insertion_ROR_8_3_1_2_r0002_0000_sella.log'):
    os.remove('conf/1642764945472630600001_r13_insertion_ROR_8_3_1_2_r0002_0000_sella.log')

sella_kwargs = {}
opt = Sella(mol, 
            order=0, 
            constraints=const,
            trajectory='conf/1642764945472630600001_r13_insertion_ROR_8_3_1_2_r0002_0000.traj', 
            logfile='conf/1642764945472630600001_r13_insertion_ROR_8_3_1_2_r0002_0000_sella.log',
            **sella_kwargs,
            )

try:
    mol.calc.label = 'conf/1642764945472630600001_r13_insertion_ROR_8_3_1_2_r0002_0000'
    opt.run(fmax=1e-4, steps=100)
    e = mol.get_potential_energy()
    db.write(mol, name='conf/1642764945472630600001_r13_insertion_ROR_8_3_1_2_r0002_0000', 
             data={'energy': e, 'status': 'normal'})
except (RuntimeError, ValueError):
    data = {'status': 'error'}
    db.write(mol, name='conf/1642764945472630600001_r13_insertion_ROR_8_3_1_2_r0002_0000', data=data)
with open('conf/1642764945472630600001_r13_insertion_ROR_8_3_1_2_r0002_0000.log', 'a') as f:
    f.write('done\n')
