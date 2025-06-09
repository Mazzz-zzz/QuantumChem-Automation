import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003686066703381580601_0018'
logfile = 'conf/2003686066703381580601_0018.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(5.131884246703393), np.float64(0.8950478166796051), np.float64(-1.0270901126197152)], [np.float64(3.8377611676822863), np.float64(0.9923361863836416), np.float64(-0.1772040473496337)], [np.float64(3.556321188708328), np.float64(-0.20434724184015618), np.float64(0.33114862981424054)], [np.float64(4.039110658380234), np.float64(1.8731799446033681), np.float64(0.8089013038527741)], [np.float64(2.3805687083289397), np.float64(1.6527151520107273), np.float64(-1.231318355513623)], [np.float64(0.9656734254322213), np.float64(0.0), np.float64(0.0)], [np.float64(2.217165738196346), np.float64(0.6544985456809735), np.float64(-2.285391216555191)], [np.float64(1.2422391942639175), np.float64(1.3943354573833842), np.float64(0.0)], [np.float64(5.049215244264142), np.float64(-0.08935552116842871), np.float64(-1.9071119648701842)], [np.float64(5.315607135395913), np.float64(2.0469988043956167), np.float64(-1.6796077186745872)], [np.float64(6.177749041273151), np.float64(0.6816052352036585), np.float64(-0.23679027534310115)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003686066703381580601_0018', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
