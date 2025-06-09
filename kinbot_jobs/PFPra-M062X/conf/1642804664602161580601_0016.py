import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1642804664602161580601_0016'
logfile = 'conf/1642804664602161580601_0016.log'

mol = Atoms(symbols=['C', 'O', 'C', 'C', 'F', 'F', 'F', 'F', 'F', 'O', 'H'], positions=[[np.float64(0.7086664662118585), np.float64(1.972781507046178), np.float64(1.0073158152645099)], [np.float64(0.9684535556824612), np.float64(0.0), np.float64(0.0)], [np.float64(1.0292882307512632), np.float64(3.4797374109846357), np.float64(0.8966868549617659)], [np.float64(1.858269429404863), np.float64(4.178396042535898), np.float64(1.9946922409803236)], [np.float64(2.0170363457428486), np.float64(5.461834005480383), np.float64(1.7050513454986316)], [np.float64(1.2425048159046947), np.float64(4.084007475054331), np.float64(3.169057485284143)], [np.float64(3.05906429191055), np.float64(3.6168669728236096), np.float64(2.0945386224720624)], [np.float64(1.6899882075297756), np.float64(3.644768112153133), np.float64(-0.2593678235615773)], [np.float64(-0.15028858533232237), np.float64(4.115724829984706), np.float64(0.8300604498903759)], [np.float64(1.2086901023561392), np.float64(1.422882828200659), np.float64(0.0)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1642804664602161580601_0016', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, ['C', 'O', 'C', 'C', 'F', 'F', 'F', 'F', 'F', 'O', 'H'])
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
            freq = reader_gauss.read_freq(logfile, ['C', 'O', 'C', 'C', 'F', 'F', 'F', 'F', 'F', 'O', 'H'])
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
