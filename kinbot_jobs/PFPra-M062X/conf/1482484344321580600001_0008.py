import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1482484344321580600001_0008'
logfile = 'conf/1482484344321580600001_0008.log'

mol = Atoms(symbols=['C', 'C', 'C', 'F', 'F', 'F', 'F', 'F', 'O', 'H'], positions=[[np.float64(1.5413014518805204), np.float64(0.0), np.float64(0.0)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.5294443430734265), np.float64(-0.648905404030713), np.float64(1.2932643628698988)], [np.float64(-1.8517738289558485), np.float64(-0.5888174931718586), np.float64(1.3373933073456756)], [np.float64(-0.15732135415895113), np.float64(-1.9164751398579951), np.float64(1.372743656035559)], [np.float64(-0.03607687633470921), np.float64(0.009499505071350797), np.float64(2.342731725180954)], [np.float64(-0.57271713578093), np.float64(1.2136979992467611), np.float64(-0.10401462443953041)], [np.float64(-0.40463065055773795), np.float64(-0.7411684173671694), np.float64(-1.0474067129681124)], [np.float64(1.9018362285583774), np.float64(1.2344027700912081), np.float64(0.0)], [np.float64(2.867648503648867), np.float64(1.2849591378737486), np.float64(-0.006274502384185719)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1482484344321580600001_0008', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, ['C', 'C', 'C', 'F', 'F', 'F', 'F', 'F', 'O', 'H'])
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
            freq = reader_gauss.read_freq(logfile, ['C', 'C', 'C', 'F', 'F', 'F', 'F', 'F', 'O', 'H'])
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
