import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/1312673532570400000002_0001'
logfile = 'conf/1312673532570400000002_0001.log'

mol = Atoms(symbols=['C', 'F', 'F', 'S', 'O', 'O', 'O', 'H'], positions=[[np.float64(2.055044042777171), np.float64(-0.4732914319560566), np.float64(1.6500083784914683)], [np.float64(2.073875288704431), np.float64(-1.7696002225365826), np.float64(1.843147983499044)], [np.float64(1.4889334697151875), np.float64(0.16094230744450905), np.float64(2.6474115294842884)], [np.float64(1.4313946355498892), np.float64(0.0), np.float64(0.0)], [np.float64(2.2260837378092453), np.float64(-0.7250198169861256), np.float64(-0.9515301621039787)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(1.8830616705612604), np.float64(1.538665858167405), np.float64(0.0)], [np.float64(1.8685605967550418), np.float64(1.8878774123234838), np.float64(0.900254402892517)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1312673532570400000002_0001', 'Symm': 'None', 'mult': 2, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, ['C', 'F', 'F', 'S', 'O', 'O', 'O', 'H'])
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
            freq = reader_gauss.read_freq(logfile, ['C', 'F', 'F', 'S', 'O', 'O', 'O', 'H'])
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
