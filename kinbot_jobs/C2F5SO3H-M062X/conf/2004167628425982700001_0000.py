import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/2004167628425982700001_0000'
logfile = 'conf/2004167628425982700001_0000.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.7876147763177229), np.float64(0.3247803841564933), np.float64(-1.2851516727461176)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.33359038399325086), np.float64(0.9055565130631729), np.float64(0.9345154716060637)], [np.float64(-0.3715793163820378), np.float64(-1.216018615008327), np.float64(0.43113373169155617)], [np.float64(1.9025159145649742), np.float64(0.0), np.float64(0.0)], [np.float64(2.0696243233940925), np.float64(-0.5448392059439247), np.float64(1.4505519500683164)], [np.float64(3.4064802274870636), np.float64(-0.1129463351679688), np.float64(0.9423916140771369)], [np.float64(1.9321182117430653), np.float64(1.5960154404061322), np.float64(0.0)], [np.float64(-0.2844418440471967), np.float64(1.4044976653747623), np.float64(-1.869306825286013)], [np.float64(-0.7513866230253705), np.float64(-0.6872218771942069), np.float64(-2.1366472357874615)], [np.float64(-2.0579893151334185), np.float64(0.5644778437736335), np.float64(-0.9765248662647321)], [np.float64(1.5797650429860157), np.float64(1.9073470736156113), np.float64(-0.8450398228432694)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2004167628425982700001_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
