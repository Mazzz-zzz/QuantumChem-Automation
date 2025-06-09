import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003716027184320770001_0015'
logfile = 'conf/2003716027184320770001_0015.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.658715803029013), np.float64(-1.351739903432076), np.float64(0.35074712500501637)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.44954833216753126), np.float64(0.4615877562753998), np.float64(-1.1394029000871608)], [np.float64(-0.46901835797943503), np.float64(0.9390504369323878), np.float64(0.9893863321819077)], [np.float64(1.9504085506544522), np.float64(0.0), np.float64(0.0)], [np.float64(-1.879387914238923), np.float64(0.4926367281860316), np.float64(1.675942032210492)], [np.float64(2.250186222116059), np.float64(-0.4194511498597054), np.float64(-1.3604472061831085)], [np.float64(2.0441409861391393), np.float64(1.6315803765466503), np.float64(0.0)], [np.float64(-0.3144764632200728), np.float64(-2.240655792679696), np.float64(-0.5734074620917634)], [np.float64(-0.2343415798841926), np.float64(-1.7683658687523023), np.float64(1.5359767741588075)], [np.float64(-1.9812987006929068), np.float64(-1.2396849951183373), np.float64(0.374305526474095)], [np.float64(2.9633179003121075), np.float64(1.8643939182829476), np.float64(-0.23423497715043048)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003716027184320770001_0015', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
