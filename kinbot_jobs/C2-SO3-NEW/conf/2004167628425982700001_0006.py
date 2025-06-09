import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2004167628425982700001_0006'
logfile = 'conf/2004167628425982700001_0006.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.7921069473789805), np.float64(0.9558092108128613), np.float64(0.9315660728817087)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.32275269439120086), np.float64(-1.2669927793222793), np.float64(0.3110827285826498)], [np.float64(-0.35866309834933563), np.float64(0.23472492599097056), np.float64(-1.27346267944019)], [np.float64(1.921470231146452), np.float64(0.0), np.float64(0.0)], [np.float64(2.1496886965003585), np.float64(-0.526311843857017), np.float64(1.4635299875227474)], [np.float64(3.5044424276411097), np.float64(-0.06435626809758313), np.float64(1.0043667966646592)], [np.float64(1.9228348966856288), np.float64(1.6177724188444942), np.float64(0.0)], [np.float64(-0.30368822566917186), np.float64(0.9023354882502146), np.float64(2.1665956260878856)], [np.float64(-0.7369881882167275), np.float64(2.2049221637889955), np.float64(0.4929670118639567)], [np.float64(-2.0703454285260765), np.float64(0.5783141373276364), np.float64(0.9645515838244053)], [np.float64(1.6024311084645493), np.float64(1.908243977296485), np.float64(-0.864453109374392)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2004167628425982700001_0006', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
