import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003716027184320770001_0022'
logfile = 'conf/2003716027184320770001_0022.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.6587158030290117), np.float64(0.3721140311573386), np.float64(-1.3460146581838106)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.44954833216753154), np.float64(0.7559579784834428), np.float64(0.9694481730539369)], [np.float64(-0.46901835797943525), np.float64(-1.3263589162928346), np.float64(0.3185483677273703)], [np.float64(1.9504085506544522), np.float64(0.0), np.float64(0.0)], [np.float64(0.5768144721332878), np.float64(-2.4971234998299674), np.float64(-0.12341338991183669)], [np.float64(2.2501862221160596), np.float64(-0.4194511498597048), np.float64(-1.3604472061831094)], [np.float64(2.0441409861391384), np.float64(1.6315803765466506), np.float64(0.0)], [np.float64(-0.3144764632200723), np.float64(1.6169133252308774), np.float64(-1.653761106551494)], [np.float64(-0.23434157988419052), np.float64(-0.4460119716682489), np.float64(-2.2994381526042367)], [np.float64(-1.9812987006929055), np.float64(0.2956844028556939), np.float64(-1.2607514616999174)], [np.float64(1.4065647916359207), np.float64(1.9538276124006846), np.float64(-0.6660388010260585)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003716027184320770001_0022', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
