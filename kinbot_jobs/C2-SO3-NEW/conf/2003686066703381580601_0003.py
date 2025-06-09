import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003686066703381580601_0003'
logfile = 'conf/2003686066703381580601_0003.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(1.55433963678643), np.float64(-0.987894364044573), np.float64(-1.959352051835567)], [np.float64(1.488755683088897), np.float64(0.48019499424208933), np.float64(-2.456280895411643)], [np.float64(2.0281804328952338), np.float64(0.5565746435513885), np.float64(-3.6698991311010047)], [np.float64(0.2070639249702202), np.float64(0.8599280257752355), np.float64(-2.4998718279813916)], [np.float64(2.38056870832894), np.float64(1.6527151520107282), np.float64(-1.231318355513622)], [np.float64(0.9656734254322212), np.float64(0.0), np.float64(0.0)], [np.float64(2.2024124537183827), np.float64(2.9819459009679186), np.float64(-1.8106390656171396)], [np.float64(1.2422391942639177), np.float64(1.3943354573833846), np.float64(0.0)], [np.float64(2.7814575627556204), np.float64(-1.4708312764293177), np.float64(-2.0655409890671006)], [np.float64(1.1785291812912118), np.float64(-1.0341523456426), np.float64(-0.6774974950234639)], [np.float64(0.7286788912015183), np.float64(-1.7448866648308172), np.float64(-2.672942779534236)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003686066703381580601_0003', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
