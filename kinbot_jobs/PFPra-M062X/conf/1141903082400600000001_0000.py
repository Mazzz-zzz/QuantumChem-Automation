import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1141903082400600000001_0000'
logfile = 'conf/1141903082400600000001_0000.log'

mol = Atoms(symbols=['C', 'O', 'C', 'F', 'F', 'F', 'O', 'H'], positions=[[np.float64(1.5439038212417897), np.float64(0.0), np.float64(0.0)], [np.float64(2.1987467015280915), np.float64(-0.9911963501499776), np.float64(0.00038207683037855267)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.46089815626705377), np.float64(0.6303844329169782), np.float64(-1.077311271025496)], [np.float64(-0.45847034529047076), np.float64(-1.2371087703753816), np.float64(-0.0024470411821635395)], [np.float64(-0.4601887992177792), np.float64(0.6258882391550206), np.float64(1.080300567056653)], [np.float64(1.9950290040726721), np.float64(1.2498921487979686), np.float64(0.0)], [np.float64(1.667814081809562), np.float64(1.6928756916407806), np.float64(-0.7949650260884298)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1141903082400600000001_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, ['C', 'O', 'C', 'F', 'F', 'F', 'O', 'H'])
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
            freq = reader_gauss.read_freq(logfile, ['C', 'O', 'C', 'F', 'F', 'F', 'O', 'H'])
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
