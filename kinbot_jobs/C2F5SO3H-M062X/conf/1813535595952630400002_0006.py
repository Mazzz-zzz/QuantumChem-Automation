import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/1813535595952630400002_0006'
logfile = 'conf/1813535595952630400002_0006.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'H'], positions=[[np.float64(-0.5470970123072487), np.float64(-1.3878030263922165), np.float64(-0.2263813662607561)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.40572418218556794), np.float64(0.7947115628284517), np.float64(-1.0006224950412672)], [np.float64(-0.42966550034062856), np.float64(0.524711896255993), np.float64(1.1562657619191519)], [np.float64(1.8387160554772999), np.float64(0.0), np.float64(0.0)], [np.float64(2.2824008361995896), np.float64(-0.49933978520351113), np.float64(1.2435660020350048)], [np.float64(2.2336612761837635), np.float64(-0.5435452659020774), np.float64(-1.2517678239120706)], [np.float64(2.0903220202274744), np.float64(1.5514539202135955), np.float64(0.0)], [np.float64(-0.14051932431564607), np.float64(-2.2822472135440814), np.float64(0.6407121687927824)], [np.float64(-1.8471929854657931), np.float64(-1.4195842225342459), np.float64(-0.40145679684346053)], [np.float64(1.3913834218441847), np.float64(2.004922493600876), np.float64(0.4930873343902754)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1813535595952630400002_0006', 'Symm': 'None', 'mult': 2, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, ['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'H'])
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
            freq = reader_gauss.read_freq(logfile, ['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'H'])
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
