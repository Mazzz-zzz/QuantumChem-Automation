import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/1813535595952630400002_0002'
logfile = 'conf/1813535595952630400002_0002.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'H'], positions=[[np.float64(-0.5470970123072487), np.float64(0.49784949907086345), np.float64(1.3150633594349634)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.4057241821855678), np.float64(-1.2639202817181325), np.float64(-0.18792915457003834)], [np.float64(-0.4296655003406286), np.float64(0.7389995752201585), np.float64(-1.032546712785171)], [np.float64(1.8387160554772999), np.float64(0.0), np.float64(0.0)], [np.float64(2.282400836199592), np.float64(-0.4993397852035114), np.float64(1.243566002035004)], [np.float64(2.233661276183764), np.float64(-0.5435452659020769), np.float64(-1.2517678239120709)], [np.float64(2.0903220202274744), np.float64(1.5514539202135957), np.float64(0.0)], [np.float64(-0.14051932431564604), np.float64(1.6959966214604145), np.float64(1.6561279802490307)], [np.float64(-1.8471929854657931), np.float64(0.36212032667875765), np.float64(1.4301243979479688)], [np.float64(2.0988897575314875), np.float64(1.890183143731589), np.float64(-0.9069030475791703)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1813535595952630400002_0002', 'Symm': 'None', 'mult': 2, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, ['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'H'])
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
            freq = reader_gauss.read_freq(logfile, ['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'H'])
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
