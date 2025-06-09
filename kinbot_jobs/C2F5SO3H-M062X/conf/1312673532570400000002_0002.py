import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/1312673532570400000002_0002'
logfile = 'conf/1312673532570400000002_0002.log'

mol = Atoms(symbols=['C', 'F', 'F', 'S', 'O', 'O', 'O', 'H'], positions=[[np.float64(1.9238345175558818), np.float64(-0.5647364649413971), np.float64(1.617835161975108)], [np.float64(1.3451223467986178), np.float64(0.05866587485274952), np.float64(2.616295438024487)], [np.float64(3.2117650169950602), np.float64(-0.6863532818060396), np.float64(1.7965858400159462)], [np.float64(1.4192050891953565), np.float64(0.0), np.float64(0.0)], [np.float64(2.2085545746140878), np.float64(-0.7027981249257942), np.float64(-0.935510858700727)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(1.9174072337796004), np.float64(1.501722239954067), np.float64(0.0)], [np.float64(1.191958070087038), np.float64(2.0857914852309496), np.float64(0.262729162480024)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1312673532570400000002_0002', 'Symm': 'None', 'mult': 2, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
