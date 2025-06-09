import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/1502984803620600000001_0001'
logfile = 'conf/1502984803620600000001_0001.log'

mol = Atoms(symbols=['C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'H'], positions=[[np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.4334092524798718), np.float64(0.6810107902064163), np.float64(-1.0547262649091806)], [np.float64(-0.4573660175034708), np.float64(0.5614057483391757), np.float64(1.1027095816296082)], [np.float64(1.8693723367860666), np.float64(0.0), np.float64(0.0)], [np.float64(2.3001463430118556), np.float64(-0.49802291233261586), np.float64(1.2662674935182232)], [np.float64(2.2872454950681766), np.float64(-0.5442313381726379), np.float64(-1.2615745535616019)], [np.float64(2.123494334136114), np.float64(1.5837521533282353), np.float64(0.0)], [np.float64(-0.4234028570219396), np.float64(-1.2485337813807889), np.float64(-0.07639575524627079)], [np.float64(2.9381949696852656), np.float64(1.7904393909202996), np.float64(0.476416275108617)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1502984803620600000001_0001', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, ['C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'H'])
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
            freq = reader_gauss.read_freq(logfile, ['C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'H'])
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
