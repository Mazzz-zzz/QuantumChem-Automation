import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/2003846667223680600001_r12_insertion_R_9_1_10_0010'
logfile = 'conf/2003846667223680600001_r12_insertion_R_9_1_10_0010.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.23299716383686642), np.float64(-1.2287591478830313), np.float64(-0.9267801675298288)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.5654901972619116), np.float64(1.083465076894812), np.float64(-0.528836461169031)], [np.float64(-0.629128328982789), np.float64(-0.15521657972501973), np.float64(1.1432711719342887)], [np.float64(1.852147584384158), np.float64(0.0), np.float64(0.0)], [np.float64(2.853265310203649), np.float64(-0.15825948338311238), np.float64(1.0016605714075737)], [np.float64(1.7768827446278554), np.float64(-0.31649806340346087), np.float64(-1.4218757431694131)], [np.float64(1.9079594156318034), np.float64(1.6219532536408539), np.float64(0.0)], [np.float64(-0.7554833567387587), np.float64(-2.2902832377901325), np.float64(-0.5263424802842529)], [np.float64(1.3351667691397473), np.float64(-1.7836786683610597), np.float64(0.49203444163281446)], [np.float64(-0.10009146566584974), np.float64(-1.2552851419142088), np.float64(-2.178539645852687)], [np.float64(1.0987610848670086), np.float64(2.1248267475905016), np.float64(0.14665789986569927)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r12_insertion_R_9_1_10_0010', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
