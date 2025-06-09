import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/1813535595952630400002_0005'
logfile = 'conf/1813535595952630400002_0005.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'H'], positions=[[np.float64(-0.5470970123072487), np.float64(0.8899535273213516), np.float64(-1.0886819931742078)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.40572418218556777), np.float64(0.46920871888967997), np.float64(1.1885516496113062)], [np.float64(-0.4296655003406285), np.float64(-1.2637114714761515), np.float64(-0.1237190491339817)], [np.float64(1.8387160554772999), np.float64(0.0), np.float64(0.0)], [np.float64(2.2824008361995882), np.float64(-0.4993397852035102), np.float64(1.2435660020350061)], [np.float64(2.233661276183763), np.float64(-0.5435452659020783), np.float64(-1.2517678239120704)], [np.float64(2.0903220202274744), np.float64(1.5514539202135955), np.float64(0.0)], [np.float64(-0.14051932431564607), np.float64(0.5862505920836654), np.float64(-2.296840149041815)], [np.float64(-1.8471929854657931), np.float64(1.0574638958554876), np.float64(-1.028667601104509)], [np.float64(2.0988897575314875), np.float64(1.890183143731589), np.float64(-0.9069030475791703)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1813535595952630400002_0005', 'Symm': 'None', 'mult': 2, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
