import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003686066703381580601_0010'
logfile = 'conf/2003686066703381580601_0010.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(0.036524285578788174), np.float64(0.27069875130356547), np.float64(-2.429014157005397)], [np.float64(-0.1737559937460394), np.float64(1.7880186902295714), np.float64(-2.1839666074570414)], [np.float64(0.8025609886937171), np.float64(2.467559745173261), np.float64(-2.7795429988425187)], [np.float64(-1.3573956121292594), np.float64(2.1436350741223307), np.float64(-2.6952056403659754)], [np.float64(-0.23430279715327318), np.float64(2.171373660248706), np.float64(-0.307789572080636)], [np.float64(0.9656734254322222), np.float64(0.0), np.float64(0.0)], [np.float64(-1.3430407564787923), np.float64(1.3606637953599807), np.float64(0.1898610811971329)], [np.float64(1.2422391942639195), np.float64(1.394335457383384), np.float64(0.0)], [np.float64(1.2644681823781605), np.float64(-0.09746636669206721), np.float64(-2.1020114228066786)], [np.float64(-0.8358915432546831), np.float64(-0.4183696639892953), np.float64(-1.6869900706122472)], [np.float64(-0.1739116677025165), np.float64(-0.014797937711371834), np.float64(-3.7089255160592574)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003686066703381580601_0010', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
