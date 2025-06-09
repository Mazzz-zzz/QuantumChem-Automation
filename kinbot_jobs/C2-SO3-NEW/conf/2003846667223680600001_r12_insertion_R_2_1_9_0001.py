import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003846667223680600001_r12_insertion_R_2_1_9_0001'
logfile = 'conf/2003846667223680600001_r12_insertion_R_2_1_9_0001.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.07571829751833727), np.float64(-0.779467007342081), np.float64(1.3492208817095537)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.628405203776578), np.float64(-0.5590322032065367), np.float64(-1.0027648250978705)], [np.float64(-0.5078102560382912), np.float64(1.2185922655740498), np.float64(0.18556154093569394)], [np.float64(1.870398620699342), np.float64(0.0), np.float64(0.0)], [np.float64(1.947984086067542), np.float64(-0.2671887413378387), np.float64(1.46348049263798)], [np.float64(2.7409503071859294), np.float64(-0.41106966554643437), np.float64(-1.0646750446642863)], [np.float64(2.056225981402294), np.float64(1.6215329093506474), np.float64(0.0)], [np.float64(1.1203478058572849), np.float64(-1.9210418056067922), np.float64(0.03404854415042668)], [np.float64(-0.2442977712062002), np.float64(-0.06628579396466368), np.float64(2.403704741622847)], [np.float64(-0.6627311510802577), np.float64(-1.890480004658502), np.float64(1.5006780529761292)], [np.float64(2.490039259338476), np.float64(1.8788099785340826), np.float64(0.8215529266515014)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r12_insertion_R_2_1_9_0001', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')])
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
            freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')])
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
