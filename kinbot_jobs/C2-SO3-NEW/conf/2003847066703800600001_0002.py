import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003847066703800600001_0002'
logfile = 'conf/2003847066703800600001_0002.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(2.0478155592900738), np.float64(0.49220408695363027), np.float64(-2.885309314390516)], [np.float64(1.3503946836765908), np.float64(0.0), np.float64(0.0)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(1.7722704781731542), np.float64(-0.6752161935091701), np.float64(1.051494687904737)], [np.float64(1.8879906000249003), np.float64(-0.8874842606357791), np.float64(-1.5977116819296235)], [np.float64(0.8424129188112012), np.float64(-1.7634416089120473), np.float64(-2.0574443887437)], [np.float64(3.229086542962242), np.float64(-1.347734690467889), np.float64(-1.288385940966546)], [np.float64(1.873601138125437), np.float64(1.2231899022784924), np.float64(0.0)], [np.float64(2.1834910671289602), np.float64(-0.09132967742449538), np.float64(-4.061205360709814)], [np.float64(0.9485020519584451), np.float64(1.2277713070664302), np.float64(-2.8728730869979375)], [np.float64(3.099518460884611), np.float64(1.245548380308425), np.float64(-2.6361255087160798)], [np.float64(1.7510865696508615), np.float64(1.6352502836739218), np.float64(-0.8669604177802711)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003847066703800600001_0002', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
