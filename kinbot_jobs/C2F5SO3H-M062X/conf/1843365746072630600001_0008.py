import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/1843365746072630600001_0008'
logfile = 'conf/1843365746072630600001_0008.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.5946776218025803), np.float64(-1.3961407284279415), np.float64(-0.25222069297526917)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.43678944317359625), np.float64(0.8419800564615364), np.float64(-0.946346984759358)], [np.float64(-0.41025631308863697), np.float64(0.4348163901412545), np.float64(1.195277842172876)], [np.float64(1.8837227133760954), np.float64(0.0), np.float64(0.0)], [np.float64(2.2221923918609363), np.float64(-0.5094300839702787), np.float64(-1.3155307862301822)], [np.float64(1.977607310482236), np.float64(1.6018125570687785), np.float64(0.0)], [np.float64(-0.4265012744323125), np.float64(-1.765174169523796), np.float64(-1.5071365791107285)], [np.float64(0.012717833641801476), np.float64(-2.270607618209199), np.float64(0.5476903919202988)], [np.float64(-1.891427876714062), np.float64(-1.395500094840622), np.float64(0.02580111049455536)], [np.float64(1.5887863624774723), np.float64(1.9665277755185055), np.float64(-0.8120789676711521)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1843365746072630600001_0008', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, ['C', 'C', 'F', 'F', 'S', 'O', 'O', 'F', 'F', 'F', 'H'])
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
            freq = reader_gauss.read_freq(logfile, ['C', 'C', 'F', 'F', 'S', 'O', 'O', 'F', 'F', 'F', 'H'])
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
