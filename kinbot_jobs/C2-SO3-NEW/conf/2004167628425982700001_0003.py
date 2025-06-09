import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2004167628425982700001_0003'
logfile = 'conf/2004167628425982700001_0003.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.7921069473789805), np.float64(-1.2846644898256958), np.float64(0.3619720212942404)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.32275269439120063), np.float64(0.36409084402998404), np.float64(-1.2527892975958705)], [np.float64(-0.3586630983493357), np.float64(0.9854885681711189), np.float64(0.8400090885296975)], [np.float64(1.921470231146452), np.float64(0.0), np.float64(0.0)], [np.float64(2.1496886965003585), np.float64(-0.5263118438570167), np.float64(1.4635299875227479)], [np.float64(3.50444242764111), np.float64(-0.0643562680975823), np.float64(1.0043667966646588)], [np.float64(1.9228348966856288), np.float64(1.6177724188444942), np.float64(0.0)], [np.float64(-0.3036882256691719), np.float64(-2.327494596045467), np.float64(-0.3018523574830222)], [np.float64(-0.7369881882167275), np.float64(-1.5293830373963886), np.float64(1.663035101276645)], [np.float64(-2.0703454285260765), np.float64(-1.1244832435162686), np.float64(0.018558942381212636)], [np.float64(1.6024311084645495), np.float64(1.9082439772964854), np.float64(-0.8644531093743917)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2004167628425982700001_0003', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
