import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1642804254293321740001_0000'
logfile = 'conf/1642804254293321740001_0000.log'

mol = Atoms(symbols=['C', 'O', 'C', 'C', 'F', 'F', 'F', 'F', 'F', 'O', 'H'], positions=[[np.float64(1.3468408078243694), np.float64(0.0), np.float64(0.0)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(1.9968014748530694), np.float64(-1.159457257618333), np.float64(-0.08555745883195678)], [np.float64(1.431954390701454), np.float64(-2.550060887973787), np.float64(0.03539626046865235)], [np.float64(1.396277390858675), np.float64(-3.151249619299496), np.float64(-1.156791260829571)], [np.float64(2.227164105056695), np.float64(-3.2769214167904512), np.float64(0.8206908342799144)], [np.float64(0.21138661061502773), np.float64(-2.5706816887901422), np.float64(0.5471253896811494)], [np.float64(-0.3963839483742589), np.float64(0.8169645676797158), np.float64(-1.1058515183970803)], [np.float64(3.299030537081417), np.float64(-1.16609316710936), np.float64(-0.3349465946119706)], [np.float64(1.975539315887706), np.float64(1.1767070036504137), np.float64(0.0)], [np.float64(2.364658702131115), np.float64(1.3322101882763207), np.float64(0.8682994112901113)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1642804254293321740001_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, ['C', 'O', 'C', 'C', 'F', 'F', 'F', 'F', 'F', 'O', 'H'])
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
            freq = reader_gauss.read_freq(logfile, ['C', 'O', 'C', 'C', 'F', 'F', 'F', 'F', 'F', 'O', 'H'])
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
