import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003686066703381580601_0022'
logfile = 'conf/2003686066703381580601_0022.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-2.6804618370894997), np.float64(1.5028746481152564), np.float64(1.0169448088572575)], [np.float64(-1.2152580239756219), np.float64(1.0165348153846558), np.float64(0.8647040534363601)], [np.float64(-0.6456978745355542), np.float64(0.9587016139226454), np.float64(2.065511569447341)], [np.float64(-1.2238592769715355), np.float64(-0.19713720972542337), np.float64(0.30278115714088066)], [np.float64(-0.2343027971532763), np.float64(2.1713736602487046), np.float64(-0.3077895720806361)], [np.float64(0.9656734254322217), np.float64(0.0), np.float64(0.0)], [np.float64(-0.26695133699034507), np.float64(3.4717430238095908), np.float64(0.357176676193487)], [np.float64(1.2422391942639177), np.float64(1.3943354573833844), np.float64(0.0)], [np.float64(-2.739411423467885), np.float64(2.6179703072342915), np.float64(1.7264581443546965)], [np.float64(-3.1948274004195425), np.float64(1.731454209029782), np.float64(-0.19536862245219033)], [np.float64(-3.4075357316100416), np.float64(0.5685806984587907), np.float64(1.6189606761307456)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003686066703381580601_0022', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
