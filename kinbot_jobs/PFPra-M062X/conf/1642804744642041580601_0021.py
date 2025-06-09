import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1642804744642041580601_0021'
logfile = 'conf/1642804744642041580601_0021.log'

mol = Atoms(symbols=['C', 'O', 'C', 'C', 'F', 'F', 'F', 'F', 'F', 'O', 'H'], positions=[[np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(1.3589502766227322), np.float64(0.0), np.float64(0.0)], [np.float64(3.460163155941734), np.float64(1.1209912748487771), np.float64(-0.49496230215529013)], [np.float64(1.9977542410160518), np.float64(1.2255875573688642), np.float64(0.0)], [np.float64(3.9883888946217736), np.float64(2.3335101079184444), np.float64(-0.5676994755764142)], [np.float64(1.3281906368076764), np.float64(1.994786955608234), np.float64(-0.8530821498505778)], [np.float64(1.9813123138178073), np.float64(1.7936629879959416), np.float64(1.1970921458241501)], [np.float64(4.182577654332716), np.float64(0.3826378517003922), np.float64(0.32861821976079153)], [np.float64(3.479454972264886), np.float64(0.5683405248593808), np.float64(-1.7011384849785594)], [np.float64(-0.35683356779257785), np.float64(-1.2421187602782724), np.float64(0.00904051786061865)], [np.float64(-0.8942426219318236), np.float64(-1.4921724522465198), np.float64(-0.7677314469110317)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1642804744642041580601_0021', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC'}
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
