import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/1813535465033480600002_0000'
logfile = 'conf/1813535465033480600002_0000.log'

mol = Atoms(symbols=['C', 'C', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(3.393433043705972), np.float64(-0.9082635970355422), np.float64(1.9104070929803096)], [np.float64(1.9574004635149078), np.float64(-0.5359142637509051), np.float64(1.6110846939416152)], [np.float64(1.2507088406072937), np.float64(-0.09198362248511871), np.float64(2.6192850426811654)], [np.float64(1.4268282270792092), np.float64(0.0), np.float64(0.0)], [np.float64(2.23883302924779), np.float64(-0.7116607347816709), np.float64(-0.9474989204126707)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(1.8714303043710145), np.float64(1.5477021366522081), np.float64(0.0)], [np.float64(3.727912615996846), np.float64(-2.0547392366120047), np.float64(1.3312711244989368)], [np.float64(4.2366205317729655), np.float64(0.04034183315446059), np.float64(1.453608259637542)], [np.float64(3.5697633845221355), np.float64(-1.0174879640271777), np.float64(3.2214284151978125)], [np.float64(1.2849185100755993), np.float64(2.060696217415244), np.float64(-0.5719354494971094)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1813535465033480600002_0000', 'Symm': 'None', 'mult': 2, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, ['C', 'C', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'])
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
            freq = reader_gauss.read_freq(logfile, ['C', 'C', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'])
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
