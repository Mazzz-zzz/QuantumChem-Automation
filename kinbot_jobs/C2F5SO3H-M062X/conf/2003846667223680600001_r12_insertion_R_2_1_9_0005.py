import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/2003846667223680600001_r12_insertion_R_2_1_9_0005'
logfile = 'conf/2003846667223680600001_r12_insertion_R_2_1_9_0005.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(0.11394511573880012), np.float64(0.46624706918243974), np.float64(1.4808323568112438)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.892243113965492), np.float64(-0.920659486407572), np.float64(-0.28885946069513735)], [np.float64(-0.5458336878623739), np.float64(1.0123945718481089), np.float64(-0.671124815177946)], [np.float64(1.852325727138367), np.float64(0.0), np.float64(0.0)], [np.float64(2.2341080241089473), np.float64(-0.3192474607781955), np.float64(1.3710619511005275)], [np.float64(2.4282095789139566), np.float64(-0.34588692680789385), np.float64(-1.2567864706977858)], [np.float64(1.9231228026110518), np.float64(1.6214613016719097), np.float64(0.0)], [np.float64(0.7808707098550626), np.float64(-1.4493208243326716), np.float64(0.6622577519404885)], [np.float64(0.4596125809626123), np.float64(1.610697961148899), np.float64(1.8754736989565945)], [np.float64(-0.2710300359697333), np.float64(-0.2210190124653547), np.float64(2.4500484129981994)], [np.float64(1.9912805369618447), np.float64(2.116587251647356), np.float64(-0.8242458146298155)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r12_insertion_R_2_1_9_0005', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
