import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1452453943632430600002_0001'
logfile = 'conf/1452453943632430600002_0001.log'

mol = Atoms(symbols=['C', 'O', 'C', 'C', 'F', 'F', 'F', 'F', 'O', 'H'], positions=[[np.float64(1.4570606725246549), np.float64(0.0), np.float64(0.0)], [np.float64(2.118139057485114), np.float64(-1.0008455003644219), np.float64(-0.00012445224053864168)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.889647042148182), np.float64(1.217369177183715), np.float64(0.00031179165380733294)], [np.float64(-2.1635290504134157), np.float64(0.8455625726502045), np.float64(-0.0011872495054098633)], [np.float64(-0.6747507888092867), np.float64(1.9734473408506903), np.float64(1.0764529029937087)], [np.float64(-0.6729336458413054), np.float64(1.9755205045809396), np.float64(-1.0740016670638826)], [np.float64(-0.6006480560425607), np.float64(-1.1566599680790615), np.float64(0.00020135699200855942)], [np.float64(1.9437143167818753), np.float64(1.2496328122545304), np.float64(0.0)], [np.float64(1.622708359450886), np.float64(1.6912940500381837), np.float64(0.7969605363369167)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1452453943632430600002_0001', 'Symm': 'None', 'mult': 2, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, ['C', 'O', 'C', 'C', 'F', 'F', 'F', 'F', 'O', 'H'])
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
            freq = reader_gauss.read_freq(logfile, ['C', 'O', 'C', 'C', 'F', 'F', 'F', 'F', 'O', 'H'])
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
