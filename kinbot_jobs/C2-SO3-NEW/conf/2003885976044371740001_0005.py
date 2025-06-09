import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003885976044371740001_0005'
logfile = 'conf/2003885976044371740001_0005.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(2.6681878733189555), np.float64(0.0771657752960725), np.float64(-2.62500590496224)], [np.float64(2.649404638313291), np.float64(-0.5104762068996663), np.float64(-1.2431526832176925)], [np.float64(-0.4143377334272442), np.float64(0.7963214093755564), np.float64(1.0856790275079007)], [np.float64(2.867520311868806), np.float64(-1.8410145824302178), np.float64(-1.2424087188715782)], [np.float64(1.7099529511989506), np.float64(0.0), np.float64(0.0)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(1.9107935694494138), np.float64(-0.6795102801314862), np.float64(1.2424758301477739)], [np.float64(1.8163794846543888), np.float64(1.5768046120054502), np.float64(0.0)], [np.float64(2.561533633364503), np.float64(1.4153037910164283), np.float64(-2.596274519427786)], [np.float64(3.8297854580322075), np.float64(-0.23203894668095673), np.float64(-3.2075579118504183)], [np.float64(1.6957190519417016), np.float64(-0.3873861780506937), np.float64(-3.4185331488397486)], [np.float64(2.7240753394852), np.float64(1.8565061375454848), np.float64(-0.18128604713694946)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003885976044371740001_0005', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
