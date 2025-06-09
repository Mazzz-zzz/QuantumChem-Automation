import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1642804664602161580601_0024'
logfile = 'conf/1642804664602161580601_0024.log'

mol = Atoms(symbols=['C', 'O', 'C', 'C', 'F', 'F', 'F', 'F', 'F', 'O', 'H'], positions=[[np.float64(0.713132631549721), np.float64(1.9720274490757135), np.float64(-1.0099308510353262)], [np.float64(0.9684535556824612), np.float64(0.0), np.float64(0.0)], [np.float64(1.0316909233368317), np.float64(3.479331745417496), np.float64(-0.8980936830978119)], [np.float64(1.8287025700147619), np.float64(4.015534603780896), np.float64(0.30946934574608753)], [np.float64(1.990984860404199), np.float64(5.326919210136835), np.float64(0.20824356234760355)], [np.float64(1.1820327555805368), np.float64(3.7566537442163543), np.float64(1.4417271960565767)], [np.float64(3.02821692000352), np.float64(3.4448680060803385), np.float64(0.36140638733409713)], [np.float64(1.722559516441632), np.float64(3.8055375998279795), np.float64(-2.0010498649059185)], [np.float64(-0.1477448793351418), np.float64(4.119009807205767), np.float64(-0.9060752032110599)], [np.float64(1.2086901023561392), np.float64(1.422882828200659), np.float64(0.0)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1642804664602161580601_0024', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC'}
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
