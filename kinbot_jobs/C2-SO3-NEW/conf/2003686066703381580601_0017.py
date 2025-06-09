import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003686066703381580601_0017'
logfile = 'conf/2003686066703381580601_0017.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(1.5371941078412403), np.float64(4.302051121222116), np.float64(0.2731462619762779)], [np.float64(2.609768552250356), np.float64(3.4239718807348556), np.float64(0.9696279940416589)], [np.float64(3.6266851538005183), np.float64(3.229370809171264), np.float64(0.13434769260508772)], [np.float64(3.034047187786483), np.float64(4.058207964302093), np.float64(2.0680647638185516)], [np.float64(1.8576487965484685), np.float64(1.7564360655636015), np.float64(1.5391079275942579)], [np.float64(0.9656734254322226), np.float64(0.0), np.float64(0.0)], [np.float64(0.7716657655319372), np.float64(2.139462463316906), np.float64(2.4380729742747596)], [np.float64(1.2422391942639206), np.float64(1.394335457383384), np.float64(0.0)], [np.float64(1.21223482387834), np.float64(3.8060355356634754), np.float64(-0.9095170707681857)], [np.float64(0.4435056877969381), np.float64(4.349122400120319), np.float64(1.0400584725355295)], [np.float64(1.9979912672532087), np.float64(5.5372285324993005), np.float64(0.11200198669646921)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003686066703381580601_0017', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
