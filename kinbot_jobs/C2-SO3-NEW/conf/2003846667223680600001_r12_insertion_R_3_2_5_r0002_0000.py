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
            positions=[[np.float64(-0.951623), np.float64(0.436973), np.float64(1.282568)], [np.float64(0.064101), np.float64(-0.073909), np.float64(0.224435)], [np.float64(0.24911), np.float64(-1.387555), np.float64(0.457692)], [np.float64(-0.4731), np.float64(0.080317), np.float64(-0.996103)], [np.float64(2.38211), np.float64(0.333573), np.float64(-0.110826)], [np.float64(3.011228), np.float64(-0.560922), np.float64(0.800234)], [np.float64(2.465927), np.float64(0.193075), np.float64(-1.525107)], [np.float64(2.049778), np.float64(1.710644), np.float64(0.417128)], [np.float64(-2.092118), np.float64(-0.235089), np.float64(1.222125)], [np.float64(-0.428585), np.float64(0.296125), np.float64(2.499065)], [np.float64(-1.202251), np.float64(1.731214), np.float64(1.073793)], [np.float64(0.975845), np.float64(1.073592), np.float64(0.47329)]])

kwargs = {'method': 'am1', 'basis': '', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r12_insertion_R_3_2_5_r0002_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None'}
mol.calc = Gaussian(**kwargs)
if 'Gaussian' == 'Gaussian':
    mol.get_potential_energy()
    mol.calc = Gaussian(**kwargs)

const = Constraints(mol)
fix_these = [[idx - 1 for idx in fix] for fix in [[1, 2], [1, 9], [1, 10], [1, 11], [2, 3], [2, 4], [2, 5], [2, 12], [5, 6], [5, 7], [5, 8], [8, 12]]]
for fix in fix_these:
    if len(fix) == 2:
        const.fix_bond(fix)
    elif len(fix) == 4:
        const.fix_dihedral(fix)
    else:
        raise ValueError(f'Unexpected length of fix: {fix}.')

for c in [[np.int64(8), np.int64(12), np.int64(2), np.int64(5), np.float64(8.177637698751)]]:
    const.fix_dihedral((c[0]-1, c[1]-1, c[2]-1, c[3]-1), target=c[4])

if os.path.isfile('conf/2003846667223680600001_r12_insertion_R_3_2_5_r0002_0000_sella.log'):
    os.remove('conf/2003846667223680600001_r12_insertion_R_3_2_5_r0002_0000_sella.log')

sella_kwargs = {}
opt = Sella(mol, 
            order=0, 
            constraints=const,
            trajectory='conf/2003846667223680600001_r12_insertion_R_3_2_5_r0002_0000.traj', 
            logfile='conf/2003846667223680600001_r12_insertion_R_3_2_5_r0002_0000_sella.log',
            **sella_kwargs,
            )

try:
    mol.calc.label = 'conf/2003846667223680600001_r12_insertion_R_3_2_5_r0002_0000'
    opt.run(fmax=1e-4, steps=100)
    e = mol.get_potential_energy()
    db.write(mol, name='conf/2003846667223680600001_r12_insertion_R_3_2_5_r0002_0000', 
             data={'energy': e, 'status': 'normal'})
except (RuntimeError, ValueError):
    data = {'status': 'error'}
    db.write(mol, name='conf/2003846667223680600001_r12_insertion_R_3_2_5_r0002_0000', data=data)
with open('conf/2003846667223680600001_r12_insertion_R_3_2_5_r0002_0000.log', 'a') as f:
    f.write('done\n')
