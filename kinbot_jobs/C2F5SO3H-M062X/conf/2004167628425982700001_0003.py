import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/2004167628425982700001_0003'
logfile = 'conf/2004167628425982700001_0003.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.7876147763177229), np.float64(-1.2753641883924496), np.float64(0.36130777304266776)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.33359038399325086), np.float64(0.3565358821088595), np.float64(-1.2514926806781945)], [np.float64(-0.37157931638203834), np.float64(0.9813820715774355), np.float64(0.837536146226202)], [np.float64(1.9025159145649742), np.float64(0.0), np.float64(0.0)], [np.float64(2.0696243233940947), np.float64(-0.5448392059439241), np.float64(1.4505519500683164)], [np.float64(3.406480227487065), np.float64(-0.11294633516796804), np.float64(0.9423916140771345)], [np.float64(1.9321182117430653), np.float64(1.5960154404061322), np.float64(0.0)], [np.float64(-0.2844418440471967), np.float64(-2.3211160308527075), np.float64(-0.28167724512747405)], [np.float64(-0.7513866230253705), np.float64(-1.5067798465206368), np.float64(1.6634752215803443)], [np.float64(-2.057989315133419), np.float64(-1.1279342634992762), np.float64(-0.0005897194490639122)], [np.float64(1.5797650429860142), np.float64(1.9073470736156113), np.float64(-0.8450398228432686)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2004167628425982700001_0003', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
