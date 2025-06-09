import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/1843365746072630600001_0006'
logfile = 'conf/1843365746072630600001_0006.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.6566755217259781), np.float64(0.7359255945262158), np.float64(1.198453878782638)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.3228747557806909), np.float64(-1.3012814094521732), np.float64(0.07294333302452066)], [np.float64(-0.4489871084863113), np.float64(0.498164216227848), np.float64(-1.145661954115696)], [np.float64(1.9044404700832738), np.float64(0.0), np.float64(0.0)], [np.float64(2.2611505430372967), np.float64(-0.5059700231161713), np.float64(-1.3228736568587929)], [np.float64(1.906582585657945), np.float64(1.6607334069967), np.float64(0.0)], [np.float64(0.03429826834185157), np.float64(0.46249601258772544), np.float64(2.3119195256412377)], [np.float64(-0.6786914452272089), np.float64(2.0449671117039), np.float64(1.016217927912518)], [np.float64(-1.9054493083689437), np.float64(0.30934021131136585), np.float64(1.3644478043788095)], [np.float64(1.706801950900779), np.float64(1.9759681482324871), np.float64(-0.8876372574960055)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1843365746072630600001_0006', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
