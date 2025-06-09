import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/1843365746072630600001_0002'
logfile = 'conf/1843365746072630600001_0002.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.5946776218025803), np.float64(0.47964083673727287), np.float64(1.3352036845643427)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.43678944317359625), np.float64(-1.2405505578271772), np.float64(-0.25600262599586726)], [np.float64(-0.4102563130886369), np.float64(0.8177327808317306), np.float64(-0.9742009609306091)], [np.float64(1.8837227133760954), np.float64(0.0), np.float64(0.0)], [np.float64(2.2221923918609363), np.float64(-0.5094300839702791), np.float64(-1.3155307862301822)], [np.float64(1.9776073104822358), np.float64(1.601812557068778), np.float64(0.0)], [np.float64(-0.4265012744323125), np.float64(-0.4226314797207682), np.float64(2.282253962467071)], [np.float64(0.012717833641801474), np.float64(1.6096176019162354), np.float64(1.6925586834354927)], [np.float64(-1.891427876714062), np.float64(0.7200944645544455), np.float64(1.1956379778682942)], [np.float64(1.5887863624774718), np.float64(1.9665277755185047), np.float64(-0.8120789676711523)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1843365746072630600001_0002', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, ['C', 'C', 'F', 'F', 'S', 'O', 'O', 'F', 'F', 'F', 'H'])
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
            freq = reader_gauss.read_freq(logfile, ['C', 'C', 'F', 'F', 'S', 'O', 'O', 'F', 'F', 'F', 'H'])
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
