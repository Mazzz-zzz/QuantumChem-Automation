import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/1813535465033480600002_0001'
logfile = 'conf/1813535465033480600002_0001.log'

mol = Atoms(symbols=['C', 'C', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(3.3934330437059725), np.float64(-0.9082635970355424), np.float64(1.9104070929803094)], [np.float64(1.9574004635149074), np.float64(-0.535914263750905), np.float64(1.6110846939416155)], [np.float64(1.2507088406072933), np.float64(-0.0919836224851187), np.float64(2.619285042681165)], [np.float64(1.4268282270792092), np.float64(0.0), np.float64(0.0)], [np.float64(2.23883302924779), np.float64(-0.711660734781671), np.float64(-0.9474989204126705)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(1.8714303043710145), np.float64(1.5477021366522081), np.float64(0.0)], [np.float64(3.727912615996845), np.float64(-2.0547392366120043), np.float64(1.3312711244989397)], [np.float64(4.236620531772966), np.float64(0.04034183315446083), np.float64(1.4536082596375424)], [np.float64(3.5697633845221364), np.float64(-1.0174879640271781), np.float64(3.221428415197812)], [np.float64(1.8257610333641487), np.float64(1.9053305926949973), np.float64(0.8968195890206414)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1813535465033480600002_0001', 'Symm': 'None', 'mult': 2, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
