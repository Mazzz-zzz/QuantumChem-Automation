import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/1813535595952630400002_0000'
logfile = 'conf/1813535595952630400002_0000.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'H'], positions=[[np.float64(-0.5658056518188407), np.float64(0.9747118025456363), np.float64(-1.0090618459113856)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.387010728861447), np.float64(0.3670578625441778), np.float64(1.223817190545888)], [np.float64(-0.4213161129439983), np.float64(-1.2566243909418662), np.float64(-0.22365621139987113)], [np.float64(1.8732651835746588), np.float64(0.0), np.float64(0.0)], [np.float64(2.28770098936086), np.float64(-0.5614834729503739), np.float64(1.2578594499473816)], [np.float64(2.2874195395049495), np.float64(-0.5009237373918888), np.float64(-1.2705900556049974)], [np.float64(2.1737625201038226), np.float64(1.5742695632809773), np.float64(0.0)], [np.float64(-0.11466044768852662), np.float64(0.8212403187119952), np.float64(-2.243905475062104)], [np.float64(-1.8716567743358503), np.float64(1.0976823475118405), np.float64(-0.9808628898707584)], [np.float64(3.002066201796752), np.float64(1.7581160738155384), np.float64(-0.46225738489958573)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1813535595952630400002_0000', 'Symm': 'None', 'mult': 2, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
