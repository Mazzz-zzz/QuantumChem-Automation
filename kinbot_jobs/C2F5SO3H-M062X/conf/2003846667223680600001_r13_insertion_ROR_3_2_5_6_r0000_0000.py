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
            positions=[[np.float64(1.884448), np.float64(-0.990092), np.float64(-1.19728)], [np.float64(2.228564), np.float64(0.006626), np.float64(-0.116186)], [np.float64(-0.283559), np.float64(0.459891), np.float64(0.070311)], [np.float64(2.47562), np.float64(-0.537051), np.float64(1.058603)], [np.float64(1.934501), np.float64(1.656367), np.float64(-0.083359)], [np.float64(0.521491), np.float64(1.97853), np.float64(0.263028)], [np.float64(2.856505), np.float64(2.326347), np.float64(0.751152)], [np.float64(2.021527), np.float64(2.098036), np.float64(-1.568996)], [np.float64(1.278014), np.float64(-0.425623), np.float64(-2.229069)], [np.float64(3.017525), np.float64(-1.551474), np.float64(-1.644374)], [np.float64(1.129311), np.float64(-1.968632), np.float64(-0.722172)], [np.float64(2.946135), np.float64(2.216302), np.float64(-1.835677)]])

kwargs = {'method': 'am1', 'basis': '', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_r0000_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None'}
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

for c in [[np.int64(6), np.int64(5), np.int64(2), np.int64(3), np.float64(-10.469462585216988)]]:
    const.fix_dihedral((c[0]-1, c[1]-1, c[2]-1, c[3]-1), target=c[4])

if os.path.isfile('conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_r0000_0000_sella.log'):
    os.remove('conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_r0000_0000_sella.log')

sella_kwargs = {}
opt = Sella(mol, 
            order=0, 
            constraints=const,
            trajectory='conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_r0000_0000.traj', 
            logfile='conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_r0000_0000_sella.log',
            **sella_kwargs,
            )

try:
    mol.calc.label = 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_r0000_0000'
    opt.run(fmax=1e-4, steps=100)
    e = mol.get_potential_energy()
    db.write(mol, name='conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_r0000_0000', 
             data={'energy': e, 'status': 'normal'})
except (RuntimeError, ValueError):
    data = {'status': 'error'}
    db.write(mol, name='conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_r0000_0000', data=data)
with open('conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_r0000_0000.log', 'a') as f:
    f.write('done\n')
