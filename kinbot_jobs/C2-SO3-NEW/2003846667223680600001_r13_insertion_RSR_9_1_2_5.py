import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = '2003846667223680600001_r13_insertion_RSR_9_1_2_5'
logfile = '2003846667223680600001_r13_insertion_RSR_9_1_2_5.log'

atom = [np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')]
geom = [[np.float64(1.819654), np.float64(-0.083663), np.float64(-0.049423)], [np.float64(2.151172), np.float64(1.325601), np.float64(0.031638)], [np.float64(3.114583), np.float64(1.558565), np.float64(0.916288)], [np.float64(2.61951), np.float64(1.758902), np.float64(-1.127315)], [np.float64(0.573634), np.float64(2.427905), np.float64(0.575971)], [np.float64(0.466735), np.float64(2.105725), np.float64(1.952437)], [np.float64(1.170674), np.float64(3.624502), np.float64(0.093896)], [np.float64(-0.858212), np.float64(2.722234), np.float64(-0.038323)], [np.float64(-0.05715), np.float64(0.593091), np.float64(0.090619)], [np.float64(1.659025), np.float64(-0.731407), np.float64(-1.149748)], [np.float64(1.802442), np.float64(-0.874374), np.float64(0.949577)], [np.float64(-1.639146), np.float64(2.232482), np.float64(0.245667)]]
mol = Atoms(symbols=atom, positions=geom)

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'chk': '2003846667223680600001_r13_insertion_RSR_9_1_2_5', 'label': '2003846667223680600001_r13_insertion_RSR_9_1_2_5', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999', 'addsec': '1 2 F\n1 9 F\n1 10 F\n1 11 F\n2 3 F\n2 4 F\n2 5 F\n5 6 F\n5 7 F\n5 8 F\n8 12 F\n'}
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
