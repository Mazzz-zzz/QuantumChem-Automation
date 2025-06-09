import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/2003846667223680600001_r13_insertion_RSR_9_1_2_5_0000'
logfile = 'conf/2003846667223680600001_r13_insertion_RSR_9_1_2_5_0000.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.2388477336314201), np.float64(-1.3853481224656787), np.float64(-0.00010492832559579869)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.36401722223153415), np.float64(0.639765344638938), np.float64(-1.101453155735576)], [np.float64(-0.3376066884160858), np.float64(0.6381286512126662), np.float64(1.1019965229810063)], [np.float64(2.2596825609443467), np.float64(0.0), np.float64(0.0)], [np.float64(2.5865570292661473), np.float64(-0.3256623847887), np.float64(1.3421379056960119)], [np.float64(2.837384105750634), np.float64(-0.38997899297615224), np.float64(-1.2470981060059931)], [np.float64(2.6659361727314623), np.float64(1.5882715403632728), np.float64(0.0)], [np.float64(1.845340891742492), np.float64(-1.7404469198748593), np.float64(-0.11346850530054138)], [np.float64(-0.3358003522817333), np.float64(-2.045750918645607), np.float64(1.0749777489869807)], [np.float64(-0.4247888489978227), np.float64(-2.0410207634626567), np.float64(-1.0677006220872123)], [np.float64(1.8933591769580522), np.float64(2.078844218840768), np.float64(0.309703867367117)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_RSR_9_1_2_5_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')])
    zpe = reader_gauss.read_zpe(logfile)
    db.write(mol, name=label, data={'energy': e, 'frequencies': np.asarray(freq),
                                     'zpe': zpe, 'status': 'normal'})

except RuntimeError:
    for i in range(3):
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
            if i == 2:
                db.write(mol, name=label, data={'status': 'error'})
            pass
        else:
            break

with open(logfile, 'a') as f:
    f.write('done\n')
