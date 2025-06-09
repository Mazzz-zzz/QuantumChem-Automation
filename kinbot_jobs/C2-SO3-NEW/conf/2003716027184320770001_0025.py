import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003716027184320770001_0025'
logfile = 'conf/2003716027184320770001_0025.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.6587158030290117), np.float64(-1.3517399034320767), np.float64(0.3507471250050166)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.4495483321675313), np.float64(0.46158775627540033), np.float64(-1.1394029000871606)], [np.float64(-0.4690183579794349), np.float64(0.9390504369323865), np.float64(0.9893863321819083)], [np.float64(1.9504085506544522), np.float64(0.0), np.float64(0.0)], [np.float64(0.5768144721332878), np.float64(1.141682619084179), np.float64(2.224279082195776)], [np.float64(2.2501862221160587), np.float64(-0.4194511498597048), np.float64(-1.3604472061831097)], [np.float64(2.0441409861391384), np.float64(1.6315803765466503), np.float64(0.0)], [np.float64(-0.3144764632200723), np.float64(-2.240655792679696), np.float64(-0.5734074620917634)], [np.float64(-0.23434157988419052), np.float64(-1.7683658687523038), np.float64(1.5359767741588062)], [np.float64(-1.9812987006929055), np.float64(-1.2396849951183393), np.float64(0.37430552647409554)], [np.float64(1.40656479163592), np.float64(1.9538276124006844), np.float64(-0.6660388010260581)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003716027184320770001_0025', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
