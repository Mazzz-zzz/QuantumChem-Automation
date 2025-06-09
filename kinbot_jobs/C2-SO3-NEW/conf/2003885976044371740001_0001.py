import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003885976044371740001_0001'
logfile = 'conf/2003885976044371740001_0001.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(2.668187873318957), np.float64(0.07716577529607316), np.float64(-2.6250059049622383)], [np.float64(2.649404638313292), np.float64(-0.5104762068996664), np.float64(-1.2431526832176918)], [np.float64(-0.41433773342724467), np.float64(-1.338386322865605), np.float64(0.14679505634270892)], [np.float64(2.867520311868806), np.float64(-1.8410145824302173), np.float64(-1.2424087188715776)], [np.float64(1.7099529511989506), np.float64(0.0), np.float64(0.0)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(1.9107935694494136), np.float64(-0.6795102801314867), np.float64(1.2424758301477739)], [np.float64(1.8163794846543888), np.float64(1.5768046120054502), np.float64(0.0)], [np.float64(2.5615336333645033), np.float64(1.4153037910164292), np.float64(-2.5962745194277854)], [np.float64(3.8297854580322093), np.float64(-0.2320389466809551), np.float64(-3.2075579118504165)], [np.float64(1.695719051941702), np.float64(-0.3873861780506936), np.float64(-3.418533148839748)], [np.float64(1.553537277137599), np.float64(1.9355116828773564), np.float64(0.8586341190560728)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003885976044371740001_0001', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
