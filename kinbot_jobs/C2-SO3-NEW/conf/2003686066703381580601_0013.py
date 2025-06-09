import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003686066703381580601_0013'
logfile = 'conf/2003686066703381580601_0013.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.5680008094996043), np.float64(0.9849279081453497), np.float64(2.2741667156585694)], [np.float64(-1.2152580239756205), np.float64(1.0165348153846594), np.float64(0.8647040534363623)], [np.float64(-1.2710503968292497), np.float64(-0.22114738387306154), np.float64(0.3802330859863692)], [np.float64(-2.448643368017696), np.float64(1.5225954873855163), np.float64(0.9719155118969683)], [np.float64(-0.23430279715327296), np.float64(2.171373660248707), np.float64(-0.3077895720806346)], [np.float64(0.9656734254322226), np.float64(0.0), np.float64(0.0)], [np.float64(-0.26695133699033785), np.float64(3.471743023809593), np.float64(0.3571766761934895)], [np.float64(1.24223919426392), np.float64(1.3943354573833842), np.float64(0.0)], [np.float64(0.5823933591217548), np.float64(0.33185373242344807), np.float64(2.253919894275056)], [np.float64(-0.3491620534168204), np.float64(2.2380591023694687), np.float64(2.684405930068372)], [np.float64(-1.3867454115515214), np.float64(0.3916009740188491), np.float64(3.1353201066162395)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003686066703381580601_0013', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
