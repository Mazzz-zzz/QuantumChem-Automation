import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/1843365746072630600001_0003'
logfile = 'conf/1843365746072630600001_0003.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.5946776218025803), np.float64(0.9164998916906694), np.float64(-1.0829829915890734)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.43678944317359625), np.float64(0.39857050136564154), np.float64(1.2023496107552252)], [np.float64(-0.410256313088637), np.float64(-1.2525491709729848), np.float64(-0.22107688124226557)], [np.float64(1.8837227133760954), np.float64(0.0), np.float64(0.0)], [np.float64(2.222192391860937), np.float64(-0.5094300839702782), np.float64(-1.315530786230183)], [np.float64(1.9776073104822358), np.float64(1.601812557068778), np.float64(0.0)], [np.float64(-0.42650127443231245), np.float64(2.1878056492445648), np.float64(-0.7751173833563408)], [np.float64(0.012717833641801476), np.float64(0.6609900162929643), np.float64(-2.2402490753557935)], [np.float64(-1.8914278767140618), np.float64(0.6754056302861773), np.float64(-1.2214390883628494)], [np.float64(1.4998999094722525), np.float64(1.9717375416623417), np.float64(0.7606722781222793)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1843365746072630600001_0003', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
