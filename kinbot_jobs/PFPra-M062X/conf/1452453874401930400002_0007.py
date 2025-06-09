import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1452453874401930400002_0007'
logfile = 'conf/1452453874401930400002_0007.log'

mol = Atoms(symbols=['C', 'O', 'C', 'C', 'F', 'F', 'F', 'F', 'O', 'H'], positions=[[np.float64(1.5461575815714903), np.float64(0.0), np.float64(0.0)], [np.float64(2.204101317607146), np.float64(-0.9885600669513458), np.float64(0.03267412850552048)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.588926897362239), np.float64(0.5343593662851162), np.float64(1.2918485913452302)], [np.float64(-0.1778424693545949), np.float64(-0.11038073171428574), np.float64(2.363181522081214)], [np.float64(-0.508706349854441), np.float64(1.8336961087139918), np.float64(1.4486901995264332)], [np.float64(-0.44822674111950245), np.float64(0.7584489047746859), np.float64(-1.0143091044925454)], [np.float64(-0.42070309448139814), np.float64(-1.2563162690014023), np.float64(-0.16490719473441628)], [np.float64(2.0003964672458525), np.float64(1.251790235540809), np.float64(0.0)], [np.float64(1.6527274361477868), np.float64(1.7027936850329393), np.float64(0.7818344598893884)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1452453874401930400002_0007', 'Symm': 'None', 'mult': 2, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC'}
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
