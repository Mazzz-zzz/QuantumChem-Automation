import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003686066703381580601_0006'
logfile = 'conf/2003686066703381580601_0006.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(0.6072150737368738), np.float64(3.8175209012523332), np.float64(-1.8265822572022796)], [np.float64(2.040806566124212), np.float64(3.536825217638647), np.float64(-1.3045178352864686)], [np.float64(2.9213370785841626), np.float64(4.151278129579898), np.float64(-2.089881298381062)], [np.float64(2.139202689332554), np.float64(4.001832489695008), np.float64(-0.054350827506601807)], [np.float64(2.3805687083289406), np.float64(1.6527151520107286), np.float64(-1.2313183555136218)], [np.float64(0.9656734254322213), np.float64(0.0), np.float64(0.0)], [np.float64(3.7351936150334604), np.float64(1.551648136562555), np.float64(-0.6937466480092469)], [np.float64(1.2422391942639175), np.float64(1.3943354573833848), np.float64(0.0)], [np.float64(0.5082165037047648), np.float64(3.538318091706085), np.float64(-3.115988178641328)], [np.float64(-0.2619402610765653), np.float64(3.0603395478739532), np.float64(-1.1499953771917204)], [np.float64(0.29784234502212037), np.float64(5.094986412066277), np.float64(-1.635964523726464)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003686066703381580601_0006', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
