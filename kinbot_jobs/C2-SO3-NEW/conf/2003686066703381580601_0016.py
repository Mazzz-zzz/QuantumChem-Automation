import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003686066703381580601_0016'
logfile = 'conf/2003686066703381580601_0016.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(1.711846497751333), np.float64(4.267408903498971), np.float64(-0.37594629529353135)], [np.float64(0.3934545077792788), np.float64(3.863576707848635), np.float64(0.33488984124481036)], [np.float64(0.5965806133002447), np.float64(3.830390590635127), np.float64(1.6491655354620374)], [np.float64(-0.5461326383560312), np.float64(4.768334914692474), np.float64(0.039221632884453794)], [np.float64(-0.2343027971532723), np.float64(2.1713736602487073), np.float64(-0.3077895720806346)], [np.float64(0.9656734254322226), np.float64(0.0), np.float64(0.0)], [np.float64(-0.40697694650885685), np.float64(2.3732456796206503), np.float64(-1.744326326265511)], [np.float64(1.2422391942639206), np.float64(1.394335457383384), np.float64(0.0)], [np.float64(2.7185290629519607), np.float64(3.5072627962124354), np.float64(0.02291541566305727)], [np.float64(1.5585921030575276), np.float64(4.127945544782321), np.float64(-1.6963960164959322)], [np.float64(1.9980845627027604), np.float64(5.537210027391655), np.float64(-0.11205690020396392)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003686066703381580601_0016', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
