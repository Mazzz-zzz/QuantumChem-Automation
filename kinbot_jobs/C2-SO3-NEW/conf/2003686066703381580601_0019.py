import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003686066703381580601_0019'
logfile = 'conf/2003686066703381580601_0019.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-1.497145372083071), np.float64(2.2099126603007093), np.float64(-2.8747429285605843)], [np.float64(-0.1737559937460433), np.float64(1.78801869022957), np.float64(-2.1839666074570396)], [np.float64(0.04025241809894525), np.float64(0.4930633114520595), np.float64(-2.400699392620662)], [np.float64(0.8268271282056763), np.float64(2.5103348412415927), np.float64(-2.6996447061984203)], [np.float64(-0.23430279715327673), np.float64(2.1713736602487046), np.float64(-0.3077895720806346)], [np.float64(0.9656734254322213), np.float64(0.0), np.float64(0.0)], [np.float64(-1.343040756478795), np.float64(1.3606637953599792), np.float64(0.18986108119713507)], [np.float64(1.2422391942639175), np.float64(1.3943354573833842), np.float64(0.0)], [np.float64(-2.489859820036741), np.float64(1.406016399840491), np.float64(-2.530371932088588)], [np.float64(-1.8031135013658643), np.float64(3.458993626429857), np.float64(-2.5104564368290605)], [np.float64(-1.350453134688565), np.float64(2.1748205240283944), np.float64(-4.194293862161498)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003686066703381580601_0019', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
