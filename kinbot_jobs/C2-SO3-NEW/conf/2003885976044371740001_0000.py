import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003885976044371740001_0000'
logfile = 'conf/2003885976044371740001_0000.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(2.6681878733189563), np.float64(0.0771657752960732), np.float64(-2.6250059049622387)], [np.float64(2.6494046383132916), np.float64(-0.5104762068996664), np.float64(-1.243152683217692)], [np.float64(-0.41433773342724467), np.float64(-1.338386322865605), np.float64(0.14679505634270892)], [np.float64(2.8675203118688057), np.float64(-1.8410145824302173), np.float64(-1.2424087188715782)], [np.float64(1.7099529511989506), np.float64(0.0), np.float64(0.0)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(1.9107935694494138), np.float64(-0.6795102801314871), np.float64(1.2424758301477739)], [np.float64(1.8163794846543888), np.float64(1.5768046120054502), np.float64(0.0)], [np.float64(2.5615336333645016), np.float64(1.4153037910164294), np.float64(-2.5962745194277854)], [np.float64(3.829785458032208), np.float64(-0.23203894668095504), np.float64(-3.207557911850417)], [np.float64(1.6957190519417034), np.float64(-0.38738617805069353), np.float64(-3.4185331488397477)], [np.float64(1.2402534174152113), np.float64(1.9566567980830938), np.float64(-0.6773480719191234)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003885976044371740001_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
