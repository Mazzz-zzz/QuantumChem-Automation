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
            positions=[[np.float64(-0.138755), np.float64(0.497464), np.float64(0.008515)], [np.float64(1.801622), np.float64(-0.190227), np.float64(0.392776)], [np.float64(2.153006), np.float64(-0.365017), np.float64(1.666249)], [np.float64(2.352508), np.float64(-1.158853), np.float64(-0.332325)], [np.float64(2.486507), np.float64(1.455033), np.float64(-0.164077)], [np.float64(3.195937), np.float64(2.303429), np.float64(0.722938)], [np.float64(2.575702), np.float64(1.563991), np.float64(-1.576347)], [np.float64(0.760882), np.float64(1.883152), np.float64(0.174678)], [np.float64(-0.512742), np.float64(-0.100768), np.float64(1.119159)], [np.float64(-1.256406), np.float64(1.289824), np.float64(-0.252615)], [np.float64(-0.09799), np.float64(-0.219325), np.float64(-1.101988)], [np.float64(0.375916), np.float64(2.633435), np.float64(-0.310324)]])

kwargs = {'method': 'am1', 'basis': '', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_ROR_1_2_5_8_r0002_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None'}
mol.calc = Gaussian(**kwargs)
if 'Gaussian' == 'Gaussian':
    mol.get_potential_energy()
    mol.calc = Gaussian(**kwargs)

const = Constraints(mol)
fix_these = [[idx - 1 for idx in fix] for fix in [[1, 2], [1, 8], [1, 9], [1, 10], [1, 11], [2, 3], [2, 4], [2, 5], [5, 6], [5, 7], [5, 8], [8, 12]]]
for fix in fix_these:
    if len(fix) == 2:
        const.fix_bond(fix)
    elif len(fix) == 4:
        const.fix_dihedral(fix)
    else:
        raise ValueError(f'Unexpected length of fix: {fix}.')

for c in [[np.int64(8), np.int64(1), np.int64(2), np.int64(5), np.float64(21.967695775934395)]]:
    const.fix_dihedral((c[0]-1, c[1]-1, c[2]-1, c[3]-1), target=c[4])

if os.path.isfile('conf/2003846667223680600001_r13_insertion_ROR_1_2_5_8_r0002_0000_sella.log'):
    os.remove('conf/2003846667223680600001_r13_insertion_ROR_1_2_5_8_r0002_0000_sella.log')

sella_kwargs = {}
opt = Sella(mol, 
            order=0, 
            constraints=const,
            trajectory='conf/2003846667223680600001_r13_insertion_ROR_1_2_5_8_r0002_0000.traj', 
            logfile='conf/2003846667223680600001_r13_insertion_ROR_1_2_5_8_r0002_0000_sella.log',
            **sella_kwargs,
            )

try:
    mol.calc.label = 'conf/2003846667223680600001_r13_insertion_ROR_1_2_5_8_r0002_0000'
    opt.run(fmax=1e-4, steps=100)
    e = mol.get_potential_energy()
    db.write(mol, name='conf/2003846667223680600001_r13_insertion_ROR_1_2_5_8_r0002_0000', 
             data={'energy': e, 'status': 'normal'})
except (RuntimeError, ValueError):
    data = {'status': 'error'}
    db.write(mol, name='conf/2003846667223680600001_r13_insertion_ROR_1_2_5_8_r0002_0000', data=data)
with open('conf/2003846667223680600001_r13_insertion_ROR_1_2_5_8_r0002_0000.log', 'a') as f:
    f.write('done\n')
