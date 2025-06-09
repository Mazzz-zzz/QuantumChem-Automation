import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1452453874401930400002_0005'
logfile = 'conf/1452453874401930400002_0005.log'

mol = Atoms(symbols=['C', 'O', 'C', 'C', 'F', 'F', 'F', 'F', 'O', 'H'], positions=[[np.float64(1.5461575815714903), np.float64(0.0), np.float64(0.0)], [np.float64(2.204101317607146), np.float64(-0.9885600669513459), np.float64(0.03267412850552061)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.5889268973622387), np.float64(-1.3859533810906695), np.float64(-0.18315550971955064)], [np.float64(-0.17784246935459486), np.float64(-1.9913848660191642), np.float64(-1.2771832787934916)], [np.float64(-0.5087063498544403), np.float64(-2.171450569360433), np.float64(0.8636823132037733)], [np.float64(-0.4482267411195028), np.float64(0.499192999393046), np.float64(1.1639905712536354)], [np.float64(-0.4207030944813981), np.float64(0.7709719544075347), np.float64(-1.005548206775689)], [np.float64(2.0003964672458525), np.float64(1.251790235540809), np.float64(0.0)], [np.float64(2.9669523480404005), np.float64(1.2258990404236698), np.float64(0.025344913215116557)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1452453874401930400002_0005', 'Symm': 'None', 'mult': 2, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC'}
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
