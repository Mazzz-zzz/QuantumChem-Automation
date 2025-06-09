import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFMS-M062X/kinbot.db')
label = 'conf/1503305764823040000001_0001'
logfile = 'conf/1503305764823040000001_0001.log'

mol = Atoms(symbols=['C', 'F', 'F', 'F', 'S', 'O', 'O', 'O', 'H'], positions=[[np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.4356737599674944), np.float64(0.44360432102414227), np.float64(-1.1760081871188213)], [np.float64(-0.5465845821162996), np.float64(0.7209252294538416), np.float64(0.9633146711966324)], [np.float64(-0.3866230263015971), np.float64(-1.267450082877607), np.float64(0.14107132947889378)], [np.float64(1.8927753061224675), np.float64(0.0), np.float64(0.0)], [np.float64(1.9902023329189729), np.float64(-0.5519248358886011), np.float64(1.453966131978298)], [np.float64(3.359046167910031), np.float64(-0.14411519222038538), np.float64(1.0106892029506584)], [np.float64(1.9586452511041632), np.float64(1.5949506419538846), np.float64(0.0)], [np.float64(1.3816545772627618), np.float64(1.9211332455174417), np.float64(0.703686191715842)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1503305764823040000001_0001', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, ['C', 'F', 'F', 'F', 'S', 'O', 'O', 'O', 'H'])
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
            freq = reader_gauss.read_freq(logfile, ['C', 'F', 'F', 'F', 'S', 'O', 'O', 'O', 'H'])
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
