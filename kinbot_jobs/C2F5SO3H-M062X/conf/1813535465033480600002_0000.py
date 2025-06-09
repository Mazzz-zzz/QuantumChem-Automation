import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/1813535465033480600002_0000'
logfile = 'conf/1813535465033480600002_0000.log'

mol = Atoms(symbols=['C', 'C', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(1.0721585159242517), np.float64(-0.24952736769474015), np.float64(2.82360041158579)], [np.float64(1.898268994139777), np.float64(-0.5623448123239482), np.float64(1.5968321511338952)], [np.float64(3.175125296409906), np.float64(-0.7611769531526283), np.float64(1.7921437385846555)], [np.float64(1.4199974145927168), np.float64(0.0), np.float64(0.0)], [np.float64(2.2136111794432853), np.float64(-0.6852354739104742), np.float64(-0.9449153774282619)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(1.922895192880448), np.float64(1.4970551772804712), np.float64(0.0)], [np.float64(0.7329318449995288), np.float64(1.0499265322896874), np.float64(2.844881201787122)], [np.float64(-0.04704023208954755), np.float64(-0.9553394027380491), np.float64(2.848871028938143)], [np.float64(1.7717823207689551), np.float64(-0.5098886353353042), np.float64(3.9170026133103963)], [np.float64(2.723148026235345), np.float64(1.5743609311429276), np.float64(0.5400271245522924)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1813535465033480600002_0000', 'Symm': 'None', 'mult': 2, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
