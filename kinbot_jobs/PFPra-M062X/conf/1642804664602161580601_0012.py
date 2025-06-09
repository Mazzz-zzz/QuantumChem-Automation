import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1642804664602161580601_0012'
logfile = 'conf/1642804664602161580601_0012.log'

mol = Atoms(symbols=['C', 'O', 'C', 'C', 'F', 'F', 'F', 'F', 'F', 'O', 'H'], positions=[[np.float64(0.7131326315497193), np.float64(1.9720274490757137), np.float64(-1.0099308510353258)], [np.float64(0.9684535556824613), np.float64(0.0), np.float64(0.0)], [np.float64(-0.8059144715074715), np.float64(1.6953357740569657), np.float64(-0.9664475802536026)], [np.float64(-1.486521216898735), np.float64(0.9243895741204402), np.float64(-2.116824020302399)], [np.float64(-2.784321133986854), np.float64(0.7966333514230715), np.float64(-1.8808038738017796)], [np.float64(-1.3286676138705762), np.float64(1.5743680780560867), np.float64(-3.2656578517904915)], [np.float64(-0.9579208022563581), np.float64(-0.2895574437399375), np.float64(-2.235595807006142)], [np.float64(-1.0349741626875786), np.float64(1.0032674562661994), np.float64(0.15996047758588827)], [np.float64(-1.4082475873559346), np.float64(2.891485589100318), np.float64(-0.8843441239010501)], [np.float64(1.2086901023561387), np.float64(1.4228828282006594), np.float64(0.0)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1642804664602161580601_0012', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC'}
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
