import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1642804443153132880001_0007'
logfile = 'conf/1642804443153132880001_0007.log'

mol = Atoms(symbols=['C', 'O', 'C', 'C', 'F', 'F', 'F', 'F', 'F', 'O', 'H'], positions=[[np.float64(1.383075625815884), np.float64(0.0), np.float64(0.0)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(2.027010559542753), np.float64(-1.1450526459091284), np.float64(0.14540208239113012)], [np.float64(-0.5773278721508573), np.float64(-0.01083732554290811), np.float64(-1.2260736291849852)], [np.float64(-0.36425430694493793), np.float64(-1.1494762081231789), np.float64(-1.8728438994098844)], [np.float64(-1.8703002949763154), np.float64(0.16376509023857458), np.float64(-1.0747518888793173)], [np.float64(-0.09596365246889912), np.float64(0.974606954300621), np.float64(-1.9998844175193466)], [np.float64(3.3295419657384806), np.float64(-1.2420429411907055), np.float64(0.21288435061006586)], [np.float64(1.4382541181105337), np.float64(-2.3069547588694257), np.float64(0.2734542199268521)], [np.float64(2.005247628827924), np.float64(1.1923978659734282), np.float64(0.0)], [np.float64(2.953964846659092), np.float64(1.073847062814596), np.float64(0.1251712723514598)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1642804443153132880001_0007', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, ['C', 'O', 'C', 'C', 'F', 'F', 'F', 'F', 'F', 'O', 'H'])
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
            freq = reader_gauss.read_freq(logfile, ['C', 'O', 'C', 'C', 'F', 'F', 'F', 'F', 'F', 'O', 'H'])
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
