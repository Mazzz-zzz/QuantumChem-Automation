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
            positions=[[np.float64(1.921181), np.float64(-0.836716), np.float64(-1.182421)], [np.float64(2.018465), np.float64(0.0352), np.float64(0.03756)], [np.float64(-0.555048), np.float64(1.032577), np.float64(-0.503797)], [np.float64(1.938426), np.float64(-0.630406), np.float64(1.187233)], [np.float64(1.762604), np.float64(1.671349), np.float64(0.20697)], [np.float64(0.310011), np.float64(2.037146), np.float64(0.585234)], [np.float64(2.587558), np.float64(2.291445), np.float64(1.188585)], [np.float64(1.995835), np.float64(2.289885), np.float64(-1.215976)], [np.float64(1.745068), np.float64(-0.125778), np.float64(-2.302721)], [np.float64(3.045017), np.float64(-1.549642), np.float64(-1.324017)], [np.float64(0.917065), np.float64(-1.705689), np.float64(-1.075421)], [np.float64(1.240568), np.float64(2.123349), np.float64(-1.803591)]])

kwargs = {'method': 'am1', 'basis': '', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_r0002_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None'}
mol.calc = Gaussian(**kwargs)
if 'Gaussian' == 'Gaussian':
    mol.get_potential_energy()
    mol.calc = Gaussian(**kwargs)

const = Constraints(mol)
fix_these = [[idx - 1 for idx in fix] for fix in [[1, 2], [1, 9], [1, 10], [1, 11], [2, 3], [2, 4], [2, 5], [3, 6], [5, 6], [5, 7], [5, 8], [8, 12]]]
for fix in fix_these:
    if len(fix) == 2:
        const.fix_bond(fix)
    elif len(fix) == 4:
        const.fix_dihedral(fix)
    else:
        raise ValueError(f'Unexpected length of fix: {fix}.')

for c in [[np.int64(2), np.int64(3), np.int64(6), np.int64(5), np.float64(30.967618410389747)]]:
    const.fix_dihedral((c[0]-1, c[1]-1, c[2]-1, c[3]-1), target=c[4])

if os.path.isfile('conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_r0002_0000_sella.log'):
    os.remove('conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_r0002_0000_sella.log')

sella_kwargs = {}
opt = Sella(mol, 
            order=0, 
            constraints=const,
            trajectory='conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_r0002_0000.traj', 
            logfile='conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_r0002_0000_sella.log',
            **sella_kwargs,
            )

try:
    mol.calc.label = 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_r0002_0000'
    opt.run(fmax=1e-4, steps=100)
    e = mol.get_potential_energy()
    db.write(mol, name='conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_r0002_0000', 
             data={'energy': e, 'status': 'normal'})
except (RuntimeError, ValueError):
    data = {'status': 'error'}
    db.write(mol, name='conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_r0002_0000', data=data)
with open('conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_r0002_0000.log', 'a') as f:
    f.write('done\n')
