import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003686066703381580601_0002'
logfile = 'conf/2003686066703381580601_0002.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.7482883149437018), np.float64(2.8982541441011893), np.float64(1.840520277037005)], [np.float64(0.12730529361601617), np.float64(1.728303328360341), np.float64(2.3611706548066733)], [np.float64(0.2256680552154584), np.float64(1.810099385980274), np.float64(3.685299162776488)], [np.float64(-0.4523744424081997), np.float64(0.5736776393184879), np.float64(2.0152775653750985)], [np.float64(1.8576487965484656), np.float64(1.7564360655636027), np.float64(1.5391079275942576)], [np.float64(0.9656734254322217), np.float64(0.0), np.float64(0.0)], [np.float64(2.5397307268638007), np.float64(0.5905179349774257), np.float64(2.095530135358056)], [np.float64(1.2422391942639182), np.float64(1.3943354573833844), np.float64(0.0)], [np.float64(-0.3159396536419887), np.float64(4.058702351213668), np.float64(2.3060921293316294)], [np.float64(-0.7007417483336198), np.float64(2.9209218838367534), np.float64(0.5049492749109958)], [np.float64(-2.009304457768446), np.float64(2.72345900016131), np.float64(2.2190036744237895)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003686066703381580601_0002', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
