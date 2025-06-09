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
            positions=[[np.float64(-0.637462), np.float64(-1.214974), np.float64(0.078421)], [np.float64(-0.036186), np.float64(0.153213), np.float64(0.51384)], [np.float64(-0.688413), np.float64(1.077858), np.float64(-0.188282)], [np.float64(-0.227007), np.float64(0.392705), np.float64(1.791805)], [np.float64(1.683684), np.float64(-0.191055), np.float64(-0.08112)], [np.float64(2.896163), np.float64(0.007572), np.float64(0.640717)], [np.float64(1.312705), np.float64(-1.199335), np.float64(-1.067686)], [np.float64(1.706795), np.float64(1.119226), np.float64(-1.038448)], [np.float64(-1.052531), np.float64(-2.095785), np.float64(0.860767)], [np.float64(1.203022), np.float64(-1.522467), np.float64(1.217796)], [np.float64(-1.177449), np.float64(-1.302362), np.float64(-1.055619)], [np.float64(2.464616), np.float64(1.655004), np.float64(-0.777984)]])

kwargs = {'method': 'am1', 'basis': '', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r12_insertion_R_9_1_10_r0000_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None'}
mol.calc = Gaussian(**kwargs)
if 'Gaussian' == 'Gaussian':
    mol.get_potential_energy()
    mol.calc = Gaussian(**kwargs)

const = Constraints(mol)
fix_these = [[idx - 1 for idx in fix] for fix in [[1, 2], [1, 7], [1, 9], [1, 10], [1, 11], [2, 3], [2, 4], [2, 5], [5, 6], [5, 7], [5, 8], [5, 10], [8, 12]]]
for fix in fix_these:
    if len(fix) == 2:
        const.fix_bond(fix)
    elif len(fix) == 4:
        const.fix_dihedral(fix)
    else:
        raise ValueError(f'Unexpected length of fix: {fix}.')

for c in [[np.int64(5), np.int64(7), np.int64(1), np.int64(2), np.float64(-18.46755545923711)]]:
    const.fix_dihedral((c[0]-1, c[1]-1, c[2]-1, c[3]-1), target=c[4])

if os.path.isfile('conf/2003846667223680600001_r12_insertion_R_9_1_10_r0000_0000_sella.log'):
    os.remove('conf/2003846667223680600001_r12_insertion_R_9_1_10_r0000_0000_sella.log')

sella_kwargs = {}
opt = Sella(mol, 
            order=0, 
            constraints=const,
            trajectory='conf/2003846667223680600001_r12_insertion_R_9_1_10_r0000_0000.traj', 
            logfile='conf/2003846667223680600001_r12_insertion_R_9_1_10_r0000_0000_sella.log',
            **sella_kwargs,
            )

try:
    mol.calc.label = 'conf/2003846667223680600001_r12_insertion_R_9_1_10_r0000_0000'
    opt.run(fmax=1e-4, steps=100)
    e = mol.get_potential_energy()
    db.write(mol, name='conf/2003846667223680600001_r12_insertion_R_9_1_10_r0000_0000', 
             data={'energy': e, 'status': 'normal'})
except (RuntimeError, ValueError):
    data = {'status': 'error'}
    db.write(mol, name='conf/2003846667223680600001_r12_insertion_R_9_1_10_r0000_0000', data=data)
with open('conf/2003846667223680600001_r12_insertion_R_9_1_10_r0000_0000.log', 'a') as f:
    f.write('done\n')
