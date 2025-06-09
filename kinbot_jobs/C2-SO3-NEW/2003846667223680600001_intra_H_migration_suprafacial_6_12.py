import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = '2003846667223680600001_intra_H_migration_suprafacial_6_12'
logfile = '2003846667223680600001_intra_H_migration_suprafacial_6_12.log'

atom = [np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')]
geom = [[np.float64(2.399146), np.float64(-1.614215), np.float64(-1.464661)], [np.float64(2.079612), np.float64(-0.285953), np.float64(-0.719152)], [np.float64(2.27142), np.float64(-0.442318), np.float64(0.590238)], [np.float64(2.954246), np.float64(0.656896), np.float64(-1.066734)], [np.float64(0.336496), np.float64(0.346954), np.float64(-1.015616)], [np.float64(-0.498302), np.float64(-0.8136), np.float64(-1.158095)], [np.float64(0.053417), np.float64(1.319566), np.float64(-0.010501)], [np.float64(0.414421), np.float64(0.933494), np.float64(-2.502888)], [np.float64(1.988711), np.float64(-2.683003), np.float64(-0.807112)], [np.float64(1.81839), np.float64(-1.672746), np.float64(-2.670982)], [np.float64(3.696129), np.float64(-1.783306), np.float64(-1.682844)], [np.float64(-0.160076), np.float64(0.106847), np.float64(-1.849741)]]
mol = Atoms(symbols=atom, positions=geom)

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'chk': '2003846667223680600001_intra_H_migration_suprafacial_6_12', 'label': '2003846667223680600001_intra_H_migration_suprafacial_6_12', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999', 'addsec': ''}
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
