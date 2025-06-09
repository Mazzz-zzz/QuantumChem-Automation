import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/1813535595952630400002_0001'
logfile = 'conf/1813535595952630400002_0001.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'H'], positions=[[np.float64(-0.5658056518188407), np.float64(0.9747118025456363), np.float64(-1.0090618459113856)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.387010728861447), np.float64(0.3670578625441778), np.float64(1.223817190545888)], [np.float64(-0.4213161129439983), np.float64(-1.2566243909418662), np.float64(-0.22365621139987113)], [np.float64(1.8732651835746588), np.float64(0.0), np.float64(0.0)], [np.float64(2.2877009893608613), np.float64(-0.5614834729503742), np.float64(1.257859449947381)], [np.float64(2.287419539504948), np.float64(-0.5009237373918884), np.float64(-1.2705900556049976)], [np.float64(2.1737625201038226), np.float64(1.5742695632809773), np.float64(0.0)], [np.float64(-0.11466044768852662), np.float64(0.8212403187119952), np.float64(-2.243905475062104)], [np.float64(-1.8716567743358503), np.float64(1.0976823475118405), np.float64(-0.9808628898707584)], [np.float64(1.4608500950026535), np.float64(2.052304150565399), np.float64(-0.44362960443615845)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1813535595952630400002_0001', 'Symm': 'None', 'mult': 2, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
