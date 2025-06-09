import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1642804664602161580601_0008'
logfile = 'conf/1642804664602161580601_0008.log'

mol = Atoms(symbols=['C', 'O', 'C', 'C', 'F', 'F', 'F', 'F', 'F', 'O', 'H'], positions=[[np.float64(2.4335064132861053), np.float64(1.681563154953246), np.float64(0.0026150357708168946)], [np.float64(0.9684535556824612), np.float64(0.0), np.float64(0.0)], [np.float64(2.563123799032126), np.float64(3.2207678368314165), np.float64(0.0014068281360462708)], [np.float64(3.2931160219500852), np.float64(3.9379834156530724), np.float64(1.156249980630276)], [np.float64(3.290972527853028), np.float64(5.248446207567556), np.float64(0.9587798228171293)], [np.float64(2.688883548581983), np.float64(3.6846907969721343), np.float64(2.3129500088952617)], [np.float64(4.554392688850552), np.float64(3.525019770766347), np.float64(1.2326351584026762)], [np.float64(3.202998105922063), np.float64(3.54828390599923), np.float64(-1.1315168706177527)], [np.float64(1.313414926183942), np.float64(3.707718116741544), np.float64(-0.03637806356645269)], [np.float64(1.2086901023561392), np.float64(1.422882828200659), np.float64(0.0)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1642804664602161580601_0008', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC'}
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
