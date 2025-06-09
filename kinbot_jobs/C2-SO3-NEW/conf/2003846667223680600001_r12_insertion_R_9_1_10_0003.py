import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003846667223680600001_r12_insertion_R_9_1_10_0003'
logfile = 'conf/2003846667223680600001_r12_insertion_R_9_1_10_0003.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.35316101083634055), np.float64(-1.3450080239241728), np.float64(0.13848128664656864)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.2822457042549052), np.float64(0.6353616891604327), np.float64(-1.1187783014335928)], [np.float64(-0.25930215018387975), np.float64(0.8360362586972129), np.float64(0.9958153021278341)], [np.float64(2.4025294927177456), np.float64(0.0), np.float64(0.0)], [np.float64(2.7033960053784063), np.float64(-0.3583180517152939), np.float64(1.3626239543316807)], [np.float64(2.8791966224605385), np.float64(-0.4455766730511623), np.float64(-1.2735627438678243)], [np.float64(2.9080116960834053), np.float64(1.5789974825960371), np.float64(0.0)], [np.float64(-0.39417042241484546), np.float64(-1.9701777721878238), np.float64(1.2487551263993133)], [np.float64(1.6993839149320489), np.float64(-1.7463119998780365), np.float64(-0.07467290655209734)], [np.float64(-0.5556368868195866), np.float64(-2.15221769475618), np.float64(-0.825195734772386)], [np.float64(3.805892621157126), np.float64(1.7750146470804604), np.float64(-0.29687167858289554)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r12_insertion_R_9_1_10_0003', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
