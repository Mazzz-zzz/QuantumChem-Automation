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
            positions=[[np.float64(1.687048), np.float64(-0.644165), np.float64(-1.261736)], [np.float64(1.966925), np.float64(0.201283), np.float64(0.006615)], [np.float64(-0.565913), np.float64(-0.085409), np.float64(0.287354)], [np.float64(2.021218), np.float64(-0.464583), np.float64(1.061957)], [np.float64(2.198412), np.float64(2.019086), np.float64(0.025708)], [np.float64(2.886638), np.float64(2.286444), np.float64(1.23644)], [np.float64(2.811128), np.float64(2.307703), np.float64(-1.221722)], [np.float64(0.745683), np.float64(2.13782), np.float64(0.065728)], [np.float64(0.944991), np.float64(0.006374), np.float64(-2.117881)], [np.float64(2.900571), np.float64(-0.849328), np.float64(-1.768557)], [np.float64(1.14832), np.float64(-1.802322), np.float64(-0.956405)], [np.float64(-0.54264), np.float64(0.846722), np.float64(0.264593)]])

kwargs = {'method': 'am1', 'basis': '', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_8_r0000_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None'}
mol.calc = Gaussian(**kwargs)
if 'Gaussian' == 'Gaussian':
    mol.get_potential_energy()
    mol.calc = Gaussian(**kwargs)

const = Constraints(mol)
fix_these = [[idx - 1 for idx in fix] for fix in [[1, 2], [1, 9], [1, 10], [1, 11], [2, 3], [2, 4], [2, 5], [2, 8], [3, 12], [5, 6], [5, 7], [5, 8], [8, 12]]]
for fix in fix_these:
    if len(fix) == 2:
        const.fix_bond(fix)
    elif len(fix) == 4:
        const.fix_dihedral(fix)
    else:
        raise ValueError(f'Unexpected length of fix: {fix}.')

for c in [[np.int64(3), np.int64(12), np.int64(8), np.int64(5), np.float64(-6.7395939370901425)]]:
    const.fix_dihedral((c[0]-1, c[1]-1, c[2]-1, c[3]-1), target=c[4])

if os.path.isfile('conf/2003846667223680600001_r13_insertion_ROR_3_2_5_8_r0000_0000_sella.log'):
    os.remove('conf/2003846667223680600001_r13_insertion_ROR_3_2_5_8_r0000_0000_sella.log')

sella_kwargs = {}
opt = Sella(mol, 
            order=0, 
            constraints=const,
            trajectory='conf/2003846667223680600001_r13_insertion_ROR_3_2_5_8_r0000_0000.traj', 
            logfile='conf/2003846667223680600001_r13_insertion_ROR_3_2_5_8_r0000_0000_sella.log',
            **sella_kwargs,
            )

try:
    mol.calc.label = 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_8_r0000_0000'
    opt.run(fmax=1e-4, steps=100)
    e = mol.get_potential_energy()
    db.write(mol, name='conf/2003846667223680600001_r13_insertion_ROR_3_2_5_8_r0000_0000', 
             data={'energy': e, 'status': 'normal'})
except (RuntimeError, ValueError):
    data = {'status': 'error'}
    db.write(mol, name='conf/2003846667223680600001_r13_insertion_ROR_3_2_5_8_r0000_0000', data=data)
with open('conf/2003846667223680600001_r13_insertion_ROR_3_2_5_8_r0000_0000.log', 'a') as f:
    f.write('done\n')
