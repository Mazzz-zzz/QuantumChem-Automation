import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2004167628425982700001_0001'
logfile = 'conf/2004167628425982700001_0001.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.7921069473789805), np.float64(0.3288552790128351), np.float64(-1.293538094175948)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.32275269439120063), np.float64(0.9029019352922941), np.float64(0.94170656901322)], [np.float64(-0.3586630983493354), np.float64(-1.2202134941620892), np.float64(0.433453590910492)], [np.float64(1.921470231146452), np.float64(0.0), np.float64(0.0)], [np.float64(2.1496886965003585), np.float64(-0.5263118438570171), np.float64(1.4635299875227472)], [np.float64(3.50444242764111), np.float64(-0.06435626809758314), np.float64(1.0043667966646597)], [np.float64(1.9228348966856288), np.float64(1.6177724188444942), np.float64(0.0)], [np.float64(-0.3036882256691719), np.float64(1.425159107795253), np.float64(-1.864743268604863)], [np.float64(-0.7369881882167275), np.float64(-0.6755391263926069), np.float64(-2.1560021131406013)], [np.float64(-2.0703454285260765), np.float64(0.5461691061886321), np.float64(-0.9831105262056183)], [np.float64(1.3347659010109103), np.float64(1.9084697652258584), np.float64(0.7099164748165537)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2004167628425982700001_0001', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
