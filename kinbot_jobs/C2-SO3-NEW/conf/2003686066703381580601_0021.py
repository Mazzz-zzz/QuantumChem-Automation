import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003686066703381580601_0021'
logfile = 'conf/2003686066703381580601_0021.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(2.1480591158871776), np.float64(0.5451398342950784), np.float64(-3.8590021955015397)], [np.float64(1.4887556830888953), np.float64(0.4801949942420898), np.float64(-2.4562808954116426)], [np.float64(0.19970218558201802), np.float64(0.7910169177050334), np.float64(-2.563112285883183)], [np.float64(1.6224799394752711), np.float64(-0.761707227352086), np.float64(-1.9781304978144416)], [np.float64(2.3805687083289397), np.float64(1.6527151520107277), np.float64(-1.2313183555136225)], [np.float64(0.9656734254322217), np.float64(0.0), np.float64(0.0)], [np.float64(2.202412453718382), np.float64(2.9819459009679177), np.float64(-1.8106390656171416)], [np.float64(1.2422391942639177), np.float64(1.3943354573833844), np.float64(0.0)], [np.float64(1.8906814941338537), np.float64(1.6995935990053017), np.float64(-4.451721202229008)], [np.float64(3.4713014635723125), np.float64(0.40923074792608327), np.float64(-3.728300957266878)], [np.float64(1.6914617658135849), np.float64(-0.4428030081509955), np.float64(-4.620219994079806)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003686066703381580601_0021', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
