import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = '2003846667223680600001_intra_H_migration_6_12'
logfile = '2003846667223680600001_intra_H_migration_6_12.log'

atom = [np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')]
geom = [[np.float64(2.276199), np.float64(-1.887944), np.float64(-1.506516)], [np.float64(2.369335), np.float64(-0.531461), np.float64(-0.745432)], [np.float64(2.673036), np.float64(-0.754797), np.float64(0.535347)], [np.float64(3.424621), np.float64(0.168577), np.float64(-1.166826)], [np.float64(0.832212), np.float64(0.527318), np.float64(-0.75623)], [np.float64(-0.445014), np.float64(-0.156304), np.float64(-0.819398)], [np.float64(1.061476), np.float64(1.57447), np.float64(0.161598)], [np.float64(0.400145), np.float64(1.008377), np.float64(-2.238104)], [np.float64(1.520668), np.float64(-2.770313), np.float64(-0.880546)], [np.float64(1.732583), np.float64(-1.751167), np.float64(-2.722876)], [np.float64(3.457465), np.float64(-2.462583), np.float64(-1.686299)], [np.float64(-0.571306), np.float64(0.402839), np.float64(-1.874521)]]
mol = Atoms(symbols=atom, positions=geom)

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'chk': '2003846667223680600001_intra_H_migration_6_12', 'label': '2003846667223680600001_intra_H_migration_6_12', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999', 'addsec': ''}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy() # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')])
    zpe = reader_gauss.read_zpe(logfile)
    db.write(mol, name=label, data={'energy': e,'frequencies': np.asarray(freq), 'zpe':zpe, 'status': 'normal'})
except RuntimeError:
    try:
        iowait(logfile, 'gauss')
        mol.positions = reader_gauss.read_geom(logfile, mol)
        kwargs = reader_gauss.correct_kwargs(logfile, kwargs)
        mol.calc = Gaussian(**kwargs)
        e = mol.get_potential_energy()  # use the Gaussian optimizer
        iowait(logfile, 'gauss')
        mol.positions = reader_gauss.read_geom(logfile, mol)
        freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')])
        zpe = reader_gauss.read_zpe(logfile)
        db.write(mol, name=label, data={'energy': e,
                                         'frequencies': np.asarray(freq),
                                         'zpe': zpe, 'status': 'normal'})
    except RuntimeError:
        db.write(mol, name=label, data={'status': 'error'})

with open(logfile,'a') as f:
    f.write('done\n')
