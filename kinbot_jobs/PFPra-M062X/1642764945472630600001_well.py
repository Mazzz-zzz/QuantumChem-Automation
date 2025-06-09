import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = '1642764945472630600001_well'
logfile = '1642764945472630600001_well.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')], positions=[[np.float64(1.1353099027529996), np.float64(0.2818424042213037), np.float64(-0.04932059362590502)], [np.float64(1.9503121005395452), np.float64(0.6694059016933546), np.float64(-0.9430034254090959)], [np.float64(-0.27154693488105136), np.float64(0.7417615599514397), np.float64(-0.01608426824916408)], [np.float64(-1.2251712619010953), np.float64(-0.41740821933091626), np.float64(-0.13285556915948304)], [np.float64(-2.5184321812309323), np.float64(0.07369128584908914), np.float64(-0.09584013495396929)], [np.float64(-0.9521738478037399), np.float64(-1.1142943285030151), np.float64(-1.2946502586569213)], [np.float64(-1.0255963511231951), np.float64(-1.3060896861315279), np.float64(0.9091609772921099)], [np.float64(-0.5939033305183528), np.float64(1.4017341864250599), np.float64(1.158349364039376)], [np.float64(-0.4631597035729815), np.float64(1.5814264137533633), np.float64(-1.1049125890002949)], [np.float64(1.636390824669976), np.float64(-0.6045589216272745), np.float64(0.9050110558552964)], [np.float64(2.3279707830688103), np.float64(-1.3075105963008813), np.float64(0.6641454418680511)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'chk': '1642764945472630600001_well', 'label': '1642764945472630600001_well', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')])
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
            freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')])
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
