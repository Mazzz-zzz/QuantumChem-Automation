import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1642804664602161580601_0022'
logfile = 'conf/1642804664602161580601_0022.log'

mol = Atoms(symbols=['C', 'O', 'C', 'C', 'F', 'F', 'F', 'F', 'F', 'O', 'H'], positions=[[np.float64(0.7086664662118585), np.float64(1.9727815070461778), np.float64(1.0073158152645107)], [np.float64(0.9684535556824613), np.float64(0.0), np.float64(0.0)], [np.float64(1.3740370152257197), np.float64(1.3272773459774077), np.float64(2.2428560168431146)], [np.float64(2.439675114085451), np.float64(0.22597984996740839), np.float64(2.0625540300855554)], [np.float64(2.8789469580499514), np.float64(-0.18712102876983172), np.float64(3.2426810138769375)], [np.float64(1.9237052024805625), np.float64(-0.814983044689487), np.float64(1.4165042717813061)], [np.float64(3.472614848295256), np.float64(0.6920618180428604), np.float64(1.3675751797782278)], [np.float64(1.95213487715368), np.float64(2.324899422516647), np.float64(2.9289865188723256)], [np.float64(0.38252563663870814), np.float64(0.7986720401299969), np.float64(2.9762059720373926)], [np.float64(1.2086901023561387), np.float64(1.4228828282006594), np.float64(0.0)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1642804664602161580601_0022', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC'}
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
