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
            positions=[[np.float64(4.128664), np.float64(2.130441), np.float64(1.813476)], [np.float64(3.35135), np.float64(0.882155), np.float64(1.301936)], [np.float64(4.157781), np.float64(0.10703), np.float64(0.594528)], [np.float64(2.847413), np.float64(0.216301), np.float64(2.32457)], [np.float64(1.852568), np.float64(1.430679), np.float64(0.211838)], [np.float64(-0.425554), np.float64(1.109874), np.float64(0.419811)], [np.float64(2.350017), np.float64(2.18144), np.float64(-0.930664)], [np.float64(1.265975), np.float64(0.070388), np.float64(0.029171)], [np.float64(4.769281), np.float64(2.723454), np.float64(0.822111)], [np.float64(3.275882), np.float64(2.987759), np.float64(2.366236)], [np.float64(5.007196), np.float64(1.740866), np.float64(2.729864)], [np.float64(-1.333675), np.float64(1.020375), np.float64(0.08568)]])

kwargs = {'method': 'am1', 'basis': '', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_ROR_12_8_5_6_r0000_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None'}
mol.calc = Gaussian(**kwargs)
if 'Gaussian' == 'Gaussian':
    mol.get_potential_energy()
    mol.calc = Gaussian(**kwargs)

const = Constraints(mol)
fix_these = [[idx - 1 for idx in fix] for fix in [[1, 2], [1, 9], [1, 10], [1, 11], [2, 3], [2, 4], [2, 5], [5, 6], [5, 7], [5, 8], [6, 8], [6, 12], [8, 12]]]
for fix in fix_these:
    if len(fix) == 2:
        const.fix_bond(fix)
    elif len(fix) == 4:
        const.fix_dihedral(fix)
    else:
        raise ValueError(f'Unexpected length of fix: {fix}.')

for c in [[np.int64(5), np.int64(6), np.int64(12), np.int64(8), np.float64(-46.360717401168046)]]:
    const.fix_dihedral((c[0]-1, c[1]-1, c[2]-1, c[3]-1), target=c[4])

if os.path.isfile('conf/2003846667223680600001_r13_insertion_ROR_12_8_5_6_r0000_0000_sella.log'):
    os.remove('conf/2003846667223680600001_r13_insertion_ROR_12_8_5_6_r0000_0000_sella.log')

sella_kwargs = {}
opt = Sella(mol, 
            order=0, 
            constraints=const,
            trajectory='conf/2003846667223680600001_r13_insertion_ROR_12_8_5_6_r0000_0000.traj', 
            logfile='conf/2003846667223680600001_r13_insertion_ROR_12_8_5_6_r0000_0000_sella.log',
            **sella_kwargs,
            )

try:
    mol.calc.label = 'conf/2003846667223680600001_r13_insertion_ROR_12_8_5_6_r0000_0000'
    opt.run(fmax=1e-4, steps=100)
    e = mol.get_potential_energy()
    db.write(mol, name='conf/2003846667223680600001_r13_insertion_ROR_12_8_5_6_r0000_0000', 
             data={'energy': e, 'status': 'normal'})
except (RuntimeError, ValueError):
    data = {'status': 'error'}
    db.write(mol, name='conf/2003846667223680600001_r13_insertion_ROR_12_8_5_6_r0000_0000', data=data)
with open('conf/2003846667223680600001_r13_insertion_ROR_12_8_5_6_r0000_0000.log', 'a') as f:
    f.write('done\n')
