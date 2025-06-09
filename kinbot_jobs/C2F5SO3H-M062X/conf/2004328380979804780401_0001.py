import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/2004328380979804780401_0001'
logfile = 'conf/2004328380979804780401_0001.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(0.2248021497276011), np.float64(-0.22502506402817768), np.float64(1.5380089357864484)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.5979323289242313), np.float64(-0.9809550106942624), np.float64(-0.6254648651859382)], [np.float64(-0.5924109667882193), np.float64(1.1287600187508222), np.float64(-0.2994450966232216)], [np.float64(1.9305557029987506), np.float64(0.0), np.float64(0.0)], [np.float64(1.6167315471145562), np.float64(-0.2094357485968195), np.float64(1.5867770764150406)], [np.float64(3.2798039597229565), np.float64(-0.28610000741142316), np.float64(-0.38756038913552)], [np.float64(2.0697596398572222), np.float64(1.6341366223214333), np.float64(0.0)], [np.float64(1.4359386979410949), np.float64(-1.5601439789979479), np.float64(-0.2858421501410271)], [np.float64(-0.28084106489537075), np.float64(0.7519342640442589), np.float64(2.2718444739419668)], [np.float64(-0.25439184491395006), np.float64(-1.3785423871325506), np.float64(1.9660896887777437)], [np.float64(1.64193019896772), np.float64(1.9737675996416446), np.float64(0.7957209526515524)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2004328380979804780401_0001', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
