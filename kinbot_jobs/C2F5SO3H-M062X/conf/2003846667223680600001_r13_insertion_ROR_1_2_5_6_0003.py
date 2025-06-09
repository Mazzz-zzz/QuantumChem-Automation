import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/2003846667223680600001_r13_insertion_ROR_1_2_5_6_0003'
logfile = 'conf/2003846667223680600001_r13_insertion_ROR_1_2_5_6_0003.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.16841701874825354), np.float64(0.595694617216676), np.float64(0.28325559996639305)], [np.float64(1.7063384823181202), np.float64(-0.5398706245363202), np.float64(-0.4742848143009438)], [np.float64(2.098071169064414), np.float64(-1.6319086430237948), np.float64(0.19087734049828395)], [np.float64(1.4148643000041106), np.float64(-0.9697116885263773), np.float64(-1.718272650105296)], [np.float64(2.558691492690437), np.float64(1.0400584745627395), np.float64(-0.1760997902572141)], [np.float64(1.4189522131527355), np.float64(1.507117732536358), np.float64(0.6506314923875679)], [np.float64(3.805936965452105), np.float64(1.3257650670884864), np.float64(0.44510357365931563)], [np.float64(2.4919261405638693), np.float64(1.9968848671577146), np.float64(-1.4356537594918366)], [np.float64(-0.786755783224653), np.float64(1.6643770465739136), np.float64(0.7401242266820689)], [np.float64(-0.5180150692028503), np.float64(0.3922250221813836), np.float64(-0.9529708540158133)], [np.float64(-0.24316834247618468), np.float64(-0.38935133670401123), np.float64(1.129410133327708)], [np.float64(2.980065450406152), np.float64(2.8328984654732325), np.float64(-1.4247174983502335)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_ROR_1_2_5_6_0003', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
