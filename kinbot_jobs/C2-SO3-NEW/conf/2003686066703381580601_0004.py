import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003686066703381580601_0004'
logfile = 'conf/2003686066703381580601_0004.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-1.2424550659254827), np.float64(-0.43315147694085976), np.float64(0.31316450886346453)], [np.float64(-1.2152580239756223), np.float64(1.0165348153846567), np.float64(0.8647040534363588)], [np.float64(-2.463417270583533), np.float64(1.4474808925228126), np.float64(1.0261540681046952)], [np.float64(-0.5755128409630094), np.float64(1.015151751740225), np.float64(2.039248771791565)], [np.float64(-0.2343027971532754), np.float64(2.1713736602487055), np.float64(-0.307789572080636)], [np.float64(0.9656734254322212), np.float64(0.0), np.float64(0.0)], [np.float64(-0.2669513369903424), np.float64(3.4717430238095917), np.float64(0.3571766761934861)], [np.float64(1.2422391942639177), np.float64(1.3943354573833846), np.float64(0.0)], [np.float64(-2.0147898354954634), np.float64(-0.5194979067009111), np.float64(-0.7575202504144374)], [np.float64(-0.00022512931219043075), np.float64(-0.8003469938175201), np.float64(-0.016314839667542047)], [np.float64(-1.699382222021554), np.float64(-1.2632819082473068), np.float64(1.243791060143799)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003686066703381580601_0004', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
