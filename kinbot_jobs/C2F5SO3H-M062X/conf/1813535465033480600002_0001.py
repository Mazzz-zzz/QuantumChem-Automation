import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/1813535465033480600002_0001'
logfile = 'conf/1813535465033480600002_0001.log'

mol = Atoms(symbols=['C', 'C', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(1.0721585159242506), np.float64(-0.24952736769474004), np.float64(2.8236004115857893)], [np.float64(1.8982689941397772), np.float64(-0.5623448123239481), np.float64(1.5968321511338948)], [np.float64(3.1751252964099055), np.float64(-0.7611769531526281), np.float64(1.7921437385846561)], [np.float64(1.4199974145927168), np.float64(0.0), np.float64(0.0)], [np.float64(2.2136111794432844), np.float64(-0.6852354739104742), np.float64(-0.9449153774282625)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(1.922895192880448), np.float64(1.4970551772804712), np.float64(0.0)], [np.float64(0.7329318449995286), np.float64(1.0499265322896874), np.float64(2.8448812017871212)], [np.float64(-0.04704023208954866), np.float64(-0.9553394027380483), np.float64(2.8488710289381416)], [np.float64(1.7717823207689558), np.float64(-0.5098886353353045), np.float64(3.917002613310395)], [np.float64(2.1228254228636865), np.float64(1.7760241083412076), np.float64(-0.9056568394081059)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1813535465033480600002_0001', 'Symm': 'None', 'mult': 2, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
