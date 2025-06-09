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
            positions=[[np.float64(-0.21984), np.float64(0.509338), np.float64(0.45066)], [np.float64(1.638357), np.float64(-0.415324), np.float64(-0.583839)], [np.float64(2.553626), np.float64(-1.363862), np.float64(-0.358006)], [np.float64(1.368692), np.float64(-0.430121), np.float64(-1.904554)], [np.float64(2.314966), np.float64(1.226743), np.float64(-0.187087)], [np.float64(0.995787), np.float64(1.865762), np.float64(0.041071)], [np.float64(3.260345), np.float64(1.233283), np.float64(0.875626)], [np.float64(2.842998), np.float64(2.06563), np.float64(-1.421551)], [np.float64(-1.019282), np.float64(1.476452), np.float64(0.849078)], [np.float64(-0.847943), np.float64(-0.098699), np.float64(-0.512487)], [np.float64(0.069534), np.float64(-0.194857), np.float64(1.505294)], [np.float64(3.80125), np.float64(1.949834), np.float64(-1.496802)]])

kwargs = {'method': 'am1', 'basis': '', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_ROR_1_2_5_6_r0000_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None'}
mol.calc = Gaussian(**kwargs)
if 'Gaussian' == 'Gaussian':
    mol.get_potential_energy()
    mol.calc = Gaussian(**kwargs)

const = Constraints(mol)
fix_these = [[idx - 1 for idx in fix] for fix in [[1, 2], [1, 6], [1, 9], [1, 10], [1, 11], [2, 3], [2, 4], [2, 5], [5, 6], [5, 7], [5, 8], [8, 12]]]
for fix in fix_these:
    if len(fix) == 2:
        const.fix_bond(fix)
    elif len(fix) == 4:
        const.fix_dihedral(fix)
    else:
        raise ValueError(f'Unexpected length of fix: {fix}.')

for c in [[np.int64(5), np.int64(6), np.int64(1), np.int64(2), np.float64(-18.227339717869867)]]:
    const.fix_dihedral((c[0]-1, c[1]-1, c[2]-1, c[3]-1), target=c[4])

if os.path.isfile('conf/2003846667223680600001_r13_insertion_ROR_1_2_5_6_r0000_0000_sella.log'):
    os.remove('conf/2003846667223680600001_r13_insertion_ROR_1_2_5_6_r0000_0000_sella.log')

sella_kwargs = {}
opt = Sella(mol, 
            order=0, 
            constraints=const,
            trajectory='conf/2003846667223680600001_r13_insertion_ROR_1_2_5_6_r0000_0000.traj', 
            logfile='conf/2003846667223680600001_r13_insertion_ROR_1_2_5_6_r0000_0000_sella.log',
            **sella_kwargs,
            )

try:
    mol.calc.label = 'conf/2003846667223680600001_r13_insertion_ROR_1_2_5_6_r0000_0000'
    opt.run(fmax=1e-4, steps=100)
    e = mol.get_potential_energy()
    db.write(mol, name='conf/2003846667223680600001_r13_insertion_ROR_1_2_5_6_r0000_0000', 
             data={'energy': e, 'status': 'normal'})
except (RuntimeError, ValueError):
    data = {'status': 'error'}
    db.write(mol, name='conf/2003846667223680600001_r13_insertion_ROR_1_2_5_6_r0000_0000', data=data)
with open('conf/2003846667223680600001_r13_insertion_ROR_1_2_5_6_r0000_0000.log', 'a') as f:
    f.write('done\n')
