import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003686066703381580601_0011'
logfile = 'conf/2003686066703381580601_0011.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.6084082913620072), np.float64(0.39862081843722463), np.float64(2.0494081840723912)], [np.float64(0.12730529361601817), np.float64(1.7283033283603408), np.float64(2.3611706548066738)], [np.float64(-0.6168192457674859), np.float64(2.749093133519378), np.float64(1.9440987460179553)], [np.float64(0.31943212891552664), np.float64(1.8110370963941802), np.float64(3.68218295991731)], [np.float64(1.8576487965484674), np.float64(1.7564360655636015), np.float64(1.5391079275942579)], [np.float64(0.9656734254322222), np.float64(0.0), np.float64(0.0)], [np.float64(2.539730726863801), np.float64(0.5905179349774226), np.float64(2.0955301353580564)], [np.float64(1.2422391942639195), np.float64(1.394335457383384), np.float64(0.0)], [np.float64(-0.9802682725331957), np.float64(0.3477760318926506), np.float64(0.7807642158710664)], [np.float64(0.21134170073066905), np.float64(-0.6260878753675239), np.float64(2.303389379136154)], [np.float64(-1.684120112393408), np.float64(0.28475118254542986), np.float64(2.8200199676717466)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003686066703381580601_0011', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, ['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'])
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
            freq = reader_gauss.read_freq(logfile, ['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'])
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
