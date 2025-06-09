import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/1813535595952630400002_0005'
logfile = 'conf/1813535595952630400002_0005.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'H'], positions=[[np.float64(-0.5658056518188407), np.float64(-1.361229093821697), np.float64(-0.33959425941734955)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.387010728861447), np.float64(0.8763278453287509), np.float64(-0.9297900288950187)], [np.float64(-0.42131611294399834), np.float64(0.434620234684462), np.float64(1.2000967512707397)], [np.float64(1.8732651835746588), np.float64(0.0), np.float64(0.0)], [np.float64(2.2877009893608604), np.float64(-0.5614834729503725), np.float64(1.2578594499473819)], [np.float64(2.287419539504948), np.float64(-0.5009237373918879), np.float64(-1.2705900556049974)], [np.float64(2.1737625201038226), np.float64(1.5742695632809773), np.float64(0.0)], [np.float64(-0.11466044768852662), np.float64(-2.353899304450769), np.float64(0.4107377589144353)], [np.float64(-1.8716567743358503), np.float64(-1.3982933540134153), np.float64(-0.46018935329561245)], [np.float64(2.2473041841757055), np.float64(1.9021854132086053), np.float64(0.9058869893357445)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1813535595952630400002_0005', 'Symm': 'None', 'mult': 2, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
