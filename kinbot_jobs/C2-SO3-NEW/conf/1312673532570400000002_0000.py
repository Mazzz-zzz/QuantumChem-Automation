import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/1312673532570400000002_0000'
logfile = 'conf/1312673532570400000002_0000.log'

mol = Atoms(symbols=['C', 'F', 'F', 'S', 'O', 'O', 'O', 'H'], positions=[[np.float64(2.0550440427771712), np.float64(-0.4732914319560568), np.float64(1.650008378491468)], [np.float64(2.0738752887044303), np.float64(-1.7696002225365826), np.float64(1.8431479834990439)], [np.float64(1.4889334697151853), np.float64(0.16094230744450946), np.float64(2.6474115294842875)], [np.float64(1.4313946355498892), np.float64(0.0), np.float64(0.0)], [np.float64(2.2260837378092453), np.float64(-0.7250198169861256), np.float64(-0.9515301621039781)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(1.8830616705612604), np.float64(1.538665858167405), np.float64(0.0)], [np.float64(1.2820731667386807), np.float64(2.0600376231846185), np.float64(-0.5473584579970725)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1312673532570400000002_0000', 'Symm': 'None', 'mult': 2, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, ['C', 'F', 'F', 'S', 'O', 'O', 'O', 'H'])
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
            freq = reader_gauss.read_freq(logfile, ['C', 'F', 'F', 'S', 'O', 'O', 'O', 'H'])
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
