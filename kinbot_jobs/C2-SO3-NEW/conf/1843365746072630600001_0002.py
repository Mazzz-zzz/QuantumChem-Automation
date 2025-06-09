import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/1843365746072630600001_0002'
logfile = 'conf/1843365746072630600001_0002.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.6566755217259781), np.float64(0.6699287070266525), np.float64(-1.2365571995461881)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.3228747557806908), np.float64(0.7138114841620298), np.float64(1.090471091545741)], [np.float64(-0.4489871084863119), np.float64(-1.2412544645274384), np.float64(0.14140811054816832)], [np.float64(1.9044404700832738), np.float64(0.0), np.float64(0.0)], [np.float64(2.2611505430372985), np.float64(-0.5059700231161708), np.float64(-1.3228736568587929)], [np.float64(1.906582585657945), np.float64(1.6607334069966997), np.float64(0.0)], [np.float64(0.034298268341851575), np.float64(1.7709330344167182), np.float64(-1.556493058870596)], [np.float64(-0.6786914452272089), np.float64(-0.14241301449852495), np.float64(-2.2791024325955265)], [np.float64(-1.9054493083689434), np.float64(1.026976355074266), np.float64(-0.9501203835970942)], [np.float64(2.775798091901948), np.float64(1.974589291594055), np.float64(0.2704515343080771)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1843365746072630600001_0002', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
