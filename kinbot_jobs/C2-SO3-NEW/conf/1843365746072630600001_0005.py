import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/1843365746072630600001_0005'
logfile = 'conf/1843365746072630600001_0005.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.6566755217259781), np.float64(-1.4058543015528686), np.float64(0.038103320763551066)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.3228747557806905), np.float64(0.5874699252901431), np.float64(-1.1634144245702618)], [np.float64(-0.44898710848631185), np.float64(0.7430902482995904), np.float64(1.0042538435675283)], [np.float64(1.9044404700832738), np.float64(0.0), np.float64(0.0)], [np.float64(2.2611505430372985), np.float64(-0.5059700231161717), np.float64(-1.322873656858792)], [np.float64(1.906582585657945), np.float64(1.6607334069967), np.float64(0.0)], [np.float64(0.034298268341851575), np.float64(-2.233429047004443), np.float64(-0.7554264667706411)], [np.float64(-0.6786914452272089), np.float64(-1.9025540972053736), np.float64(1.2628845046830086)], [np.float64(-1.9054493083689437), np.float64(-1.3363165663856325), np.float64(-0.4143274207817149)], [np.float64(2.775798091901948), np.float64(1.974589291594056), np.float64(0.2704515343080771)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1843365746072630600001_0005', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
