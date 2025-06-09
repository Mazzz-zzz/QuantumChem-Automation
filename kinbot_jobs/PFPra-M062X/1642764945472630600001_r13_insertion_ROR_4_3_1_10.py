import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = '1642764945472630600001_r13_insertion_ROR_4_3_1_10'
logfile = '1642764945472630600001_r13_insertion_ROR_4_3_1_10.log'

atom = [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')]
geom = [[np.float64(2.525766), np.float64(1.13732), np.float64(-0.126121)], [np.float64(3.217274), np.float64(2.034377), np.float64(-0.4217)], [np.float64(1.858162), np.float64(-0.139994), np.float64(0.032779)], [np.float64(-0.08189), np.float64(0.345577), np.float64(0.012532)], [np.float64(-0.462272), np.float64(-0.789407), np.float64(-0.394253)], [np.float64(-0.522236), np.float64(0.499677), np.float64(1.173598)], [np.float64(-0.371431), np.float64(1.173757), np.float64(-0.869628)], [np.float64(2.032864), np.float64(-0.984205), np.float64(-0.923735)], [np.float64(2.055534), np.float64(-0.747527), np.float64(1.133657)], [np.float64(0.885126), np.float64(1.975012), np.float64(0.652704)], [np.float64(0.875115), np.float64(2.899824), np.float64(0.350876)]]
mol = Atoms(symbols=atom, positions=geom)

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'chk': '1642764945472630600001_r13_insertion_ROR_4_3_1_10', 'label': '1642764945472630600001_r13_insertion_ROR_4_3_1_10', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999', 'addsec': '1 2 F\n1 3 F\n1 10 F\n3 4 F\n3 8 F\n3 9 F\n4 5 F\n4 6 F\n4 7 F\n10 11 F\n'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy() # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')])
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
        freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')])
        zpe = reader_gauss.read_zpe(logfile)
        db.write(mol, name=label, data={'energy': e,
                                         'frequencies': np.asarray(freq),
                                         'zpe': zpe, 'status': 'normal'})
    except RuntimeError:
        db.write(mol, name=label, data={'status': 'error'})

with open(logfile,'a') as f:
    f.write('done\n')
