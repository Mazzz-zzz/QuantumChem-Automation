import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/2004167628425982700001_0007'
logfile = 'conf/2004167628425982700001_0007.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.7876147763177228), np.float64(0.9505838042359569), np.float64(0.9238438997034508)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.33359038399325114), np.float64(-1.2620923951720326), np.float64(0.3169772090721303)], [np.float64(-0.3715793163820379), np.float64(0.2346365434308921), np.float64(-1.2686698779177588)], [np.float64(1.9025159145649742), np.float64(0.0), np.float64(0.0)], [np.float64(2.069624323394093), np.float64(-0.5448392059439245), np.float64(1.450551950068316)], [np.float64(3.406480227487065), np.float64(-0.11294633516796766), np.float64(0.9423916140771363)], [np.float64(1.9321182117430649), np.float64(1.5960154404061324), np.float64(0.0)], [np.float64(-0.28444184404719663), np.float64(0.9166183654779447), np.float64(2.150984070413487)], [np.float64(-0.7513866230253704), np.float64(2.1940017237148446), np.float64(0.4731720142071174)], [np.float64(-2.057989315133419), np.float64(0.5634564197256426), np.float64(0.9771145857137964)], [np.float64(1.385071645103407), np.float64(1.910958173907515), np.float64(0.7326142041371017)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2004167628425982700001_0007', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
