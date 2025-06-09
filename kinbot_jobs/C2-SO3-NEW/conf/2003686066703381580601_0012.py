import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003686066703381580601_0012'
logfile = 'conf/2003686066703381580601_0012.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.0044747289254680744), np.float64(0.8731527804991153), np.float64(-2.605856994205479)], [np.float64(1.4887556830888975), np.float64(0.48019499424209), np.float64(-2.456280895411644)], [np.float64(1.570729209957486), np.float64(-0.784813005111805), np.float64(-2.052898649900789)], [np.float64(2.08920916717676), np.float64(0.6225146147409322), np.float64(-3.6428860726027814)], [np.float64(2.380568708328942), np.float64(1.6527151520107273), np.float64(-1.2313183555136227)], [np.float64(0.9656734254322226), np.float64(0.0), np.float64(0.0)], [np.float64(2.202412453718384), np.float64(2.981945900967918), np.float64(-1.8106390656171405)], [np.float64(1.24223919426392), np.float64(1.3943354573833842), np.float64(0.0)], [np.float64(-0.6841036400397766), np.float64(0.5830628044163997), np.float64(-1.5084623956572107)], [np.float64(-0.09123310746374269), np.float64(2.1868990197195384), np.float64(-2.836222371006339)], [np.float64(-0.5429670716721744), np.float64(0.22423794523222562), np.float64(-3.631966281894032)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003686066703381580601_0012', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
