import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1452453874401930400002_0002'
logfile = 'conf/1452453874401930400002_0002.log'

mol = Atoms(symbols=['C', 'O', 'C', 'C', 'F', 'F', 'F', 'F', 'O', 'H'], positions=[[np.float64(1.5461575815714903), np.float64(0.0), np.float64(0.0)], [np.float64(2.2041013176071456), np.float64(-0.9885600669513461), np.float64(0.03267412850551975)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.588926897362239), np.float64(0.8515940148055531), np.float64(-1.10869308162568)], [np.float64(-0.17784246935459486), np.float64(2.1017655977334493), np.float64(-1.0859982432877209)], [np.float64(-0.5087063498544405), np.float64(0.3377544606464415), np.float64(-2.3123725127302057)], [np.float64(-0.44822674111950267), np.float64(-1.2576419041677318), np.float64(-0.14968146676109)], [np.float64(-0.4207030944813981), np.float64(0.48534431459386757), np.float64(1.1704554015101074)], [np.float64(2.0003964672458525), np.float64(1.251790235540809), np.float64(0.0)], [np.float64(2.9669523480404005), np.float64(1.2258990404236698), np.float64(0.025344913215116557)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1452453874401930400002_0002', 'Symm': 'None', 'mult': 2, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, ['C', 'O', 'C', 'C', 'F', 'F', 'F', 'F', 'O', 'H'])
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
            freq = reader_gauss.read_freq(logfile, ['C', 'O', 'C', 'C', 'F', 'F', 'F', 'F', 'O', 'H'])
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
