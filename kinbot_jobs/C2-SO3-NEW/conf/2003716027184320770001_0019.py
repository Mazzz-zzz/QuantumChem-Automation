import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003716027184320770001_0019'
logfile = 'conf/2003716027184320770001_0019.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.6587158030290117), np.float64(0.9796258722747386), np.float64(0.9952675331787945)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.4495483321675313), np.float64(-1.2175457347588439), np.float64(0.169954727033224)], [np.float64(-0.469018357979435), np.float64(0.3873084793604478), np.float64(-1.3079346999092782)], [np.float64(1.9504085506544522), np.float64(0.0), np.float64(0.0)], [np.float64(0.5768144721332878), np.float64(1.3554408807457878), np.float64(-2.10086569228394)], [np.float64(2.2501862221160582), np.float64(-0.4194511498597051), np.float64(-1.3604472061831092)], [np.float64(2.0441409861391384), np.float64(1.6315803765466503), np.float64(0.0)], [np.float64(-0.3144764632200723), np.float64(0.6237424674488184), np.float64(2.2271685686432567)], [np.float64(-0.23434157988419052), np.float64(2.214377840420552), np.float64(0.7634613784454289)], [np.float64(-1.9812987006929053), np.float64(0.9440005922626458), np.float64(0.8864459352258213)], [np.float64(1.4065647916359203), np.float64(1.953827612400685), np.float64(-0.6660388010260577)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003716027184320770001_0019', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
