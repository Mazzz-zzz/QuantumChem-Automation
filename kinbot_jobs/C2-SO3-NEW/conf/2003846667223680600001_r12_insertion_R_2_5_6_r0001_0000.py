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
            positions=[[np.float64(-0.930573), np.float64(-0.450889), np.float64(1.074689)], [np.float64(0.040547), np.float64(0.426352), np.float64(0.255411)], [np.float64(-0.281959), np.float64(0.420915), np.float64(-1.027087)], [np.float64(0.007252), np.float64(1.688929), np.float64(0.723024)], [np.float64(1.89153), np.float64(-0.035879), np.float64(0.531821)], [np.float64(1.905118), np.float64(2.568102), np.float64(1.159005)], [np.float64(2.063182), np.float64(-1.447261), np.float64(0.232637)], [np.float64(2.433313), np.float64(0.816777), np.float64(-0.726404)], [np.float64(-1.007921), np.float64(-1.659748), np.float64(0.543595)], [np.float64(-0.481406), np.float64(-0.546423), np.float64(2.32575)], [np.float64(-2.142185), np.float64(0.093405), np.float64(1.093496)], [np.float64(2.553524), np.float64(1.723754), np.float64(-0.367642)]])

kwargs = {'method': 'am1', 'basis': '', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r12_insertion_R_2_5_6_r0001_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None'}
mol.calc = Gaussian(**kwargs)
if 'Gaussian' == 'Gaussian':
    mol.get_potential_energy()
    mol.calc = Gaussian(**kwargs)

const = Constraints(mol)
fix_these = [[idx - 1 for idx in fix] for fix in [[1, 2], [1, 9], [1, 10], [1, 11], [2, 3], [2, 4], [2, 5], [4, 6], [5, 6], [5, 7], [5, 8], [8, 12]]]
for fix in fix_these:
    if len(fix) == 2:
        const.fix_bond(fix)
    elif len(fix) == 4:
        const.fix_dihedral(fix)
    else:
        raise ValueError(f'Unexpected length of fix: {fix}.')

for c in [[np.int64(6), np.int64(5), np.int64(2), np.int64(4), np.float64(0.0)]]:
    const.fix_dihedral((c[0]-1, c[1]-1, c[2]-1, c[3]-1), target=c[4])

if os.path.isfile('conf/2003846667223680600001_r12_insertion_R_2_5_6_r0001_0000_sella.log'):
    os.remove('conf/2003846667223680600001_r12_insertion_R_2_5_6_r0001_0000_sella.log')

sella_kwargs = {}
opt = Sella(mol, 
            order=0, 
            constraints=const,
            trajectory='conf/2003846667223680600001_r12_insertion_R_2_5_6_r0001_0000.traj', 
            logfile='conf/2003846667223680600001_r12_insertion_R_2_5_6_r0001_0000_sella.log',
            **sella_kwargs,
            )

try:
    mol.calc.label = 'conf/2003846667223680600001_r12_insertion_R_2_5_6_r0001_0000'
    opt.run(fmax=1e-4, steps=100)
    e = mol.get_potential_energy()
    db.write(mol, name='conf/2003846667223680600001_r12_insertion_R_2_5_6_r0001_0000', 
             data={'energy': e, 'status': 'normal'})
except (RuntimeError, ValueError):
    data = {'status': 'error'}
    db.write(mol, name='conf/2003846667223680600001_r12_insertion_R_2_5_6_r0001_0000', data=data)
with open('conf/2003846667223680600001_r12_insertion_R_2_5_6_r0001_0000.log', 'a') as f:
    f.write('done\n')
