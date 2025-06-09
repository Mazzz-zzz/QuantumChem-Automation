import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003716027184320770001_0008'
logfile = 'conf/2003716027184320770001_0008.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.6587158030290123), np.float64(-1.3517399034320765), np.float64(0.3507471250050165)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.4495483321675316), np.float64(0.4615877562753998), np.float64(-1.1394029000871608)], [np.float64(-0.46901835797943503), np.float64(0.9390504369323878), np.float64(0.9893863321819077)], [np.float64(1.9504085506544517), np.float64(0.0), np.float64(0.0)], [np.float64(-0.7276799896298881), np.float64(2.4305756397151703), np.float64(0.38256432895715375)], [np.float64(2.2501862221160613), np.float64(-0.4194511498597043), np.float64(-1.360447206183108)], [np.float64(2.0441409861391384), np.float64(1.6315803765466506), np.float64(0.0)], [np.float64(-0.3144764632200723), np.float64(-2.2406557926796964), np.float64(-0.5734074620917614)], [np.float64(-0.23434157988419207), np.float64(-1.7683658687523023), np.float64(1.5359767741588075)], [np.float64(-1.9812987006929068), np.float64(-1.2396849951183373), np.float64(0.374305526474095)], [np.float64(1.8116038338461915), np.float64(1.9305585804617804), np.float64(0.9002737781764886)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003716027184320770001_0008', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
