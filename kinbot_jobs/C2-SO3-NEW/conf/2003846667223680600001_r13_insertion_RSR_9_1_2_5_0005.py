import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003846667223680600001_r13_insertion_RSR_9_1_2_5_0005'
logfile = 'conf/2003846667223680600001_r13_insertion_RSR_9_1_2_5_0005.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.3121659232025107), np.float64(1.2977844086753103), np.float64(0.4711431922057794)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.31279364866339293), np.float64(-1.0343602491827781), np.float64(0.7682291072827169)], [np.float64(-0.39966433082063985), np.float64(-0.31927102804595436), np.float64(-1.219986184824067)], [np.float64(2.3019423409188198), np.float64(0.0), np.float64(0.0)], [np.float64(2.261071199978791), np.float64(-0.5811791068698298), np.float64(1.316240648278854)], [np.float64(2.2394969121866515), np.float64(-0.5141472662374408), np.float64(-1.3422813941711138)], [np.float64(3.7046811076628647), np.float64(0.7865449904722901), np.float64(0.0)], [np.float64(1.5840961381141487), np.float64(1.82150758903256), np.float64(0.28531216540278465)], [np.float64(-0.6498749990756981), np.float64(2.286442807429564), np.float64(-0.26569170858116425)], [np.float64(-0.33845490887738877), np.float64(1.6413975485932666), np.float64(1.7000871388617116)], [np.float64(3.9920466196716182), np.float64(1.2931858674587948), np.float64(0.7708107576643509)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_RSR_9_1_2_5_0005', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
