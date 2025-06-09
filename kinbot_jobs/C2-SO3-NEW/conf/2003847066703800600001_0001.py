import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003847066703800600001_0001'
logfile = 'conf/2003847066703800600001_0001.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(2.0478155592900715), np.float64(0.4922040869536305), np.float64(-2.8853093143905157)], [np.float64(1.3503946836765908), np.float64(0.0), np.float64(0.0)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(1.7722704781731546), np.float64(-0.6752161935091701), np.float64(1.0514946879047367)], [np.float64(1.8879906000248992), np.float64(-0.8874842606357787), np.float64(-1.597711681929624)], [np.float64(0.8424129188112021), np.float64(-1.7634416089120475), np.float64(-2.0574443887436993)], [np.float64(3.22908654296224), np.float64(-1.3477346904678886), np.float64(-1.2883859409665468)], [np.float64(1.873601138125437), np.float64(1.2231899022784924), np.float64(0.0)], [np.float64(2.1834910671289576), np.float64(-0.09132967742449416), np.float64(-4.061205360709814)], [np.float64(0.9485020519584434), np.float64(1.2277713070664305), np.float64(-2.8728730869979366)], [np.float64(3.099518460884612), np.float64(1.2455483803084253), np.float64(-2.6361255087160793)], [np.float64(2.8202379101183643), np.float64(1.1779321836199255), np.float64(0.19558758706685)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003847066703800600001_0001', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
