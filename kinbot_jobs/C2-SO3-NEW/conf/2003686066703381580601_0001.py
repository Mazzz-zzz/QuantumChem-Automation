import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003686066703381580601_0001'
logfile = 'conf/2003686066703381580601_0001.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(0.9915173065042702), np.float64(2.5531645340180944), np.float64(-2.864566245961133)], [np.float64(-0.17375599374604053), np.float64(1.7880186902295716), np.float64(-2.183966607457041)], [np.float64(-1.318753064429941), np.float64(2.116434573895671), np.float64(-2.776256105094049)], [np.float64(0.046472222149973486), np.float64(0.4747316427994279), np.float64(-2.3088976742277705)], [np.float64(-0.23430279715327473), np.float64(2.171373660248706), np.float64(-0.30778957208063606)], [np.float64(0.9656734254322217), np.float64(0.0), np.float64(0.0)], [np.float64(-1.3430407564787932), np.float64(1.3606637953599816), np.float64(0.18986108119713313)], [np.float64(1.2422391942639182), np.float64(1.3943354573833844), np.float64(0.0)], [np.float64(0.7365916691221985), np.float64(3.849933268452201), np.float64(-2.9256098760015137)], [np.float64(2.1114685791202827), np.float64(2.3631213149634105), np.float64(-2.160210422532301)], [np.float64(1.1788750712193914), np.float64(2.091085120590983), np.float64(-4.095559511822003)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003686066703381580601_0001', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
