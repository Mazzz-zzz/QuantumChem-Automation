import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1642764945472630600001_ketoenol_2_1_3_8_0003'
logfile = 'conf/1642764945472630600001_ketoenol_2_1_3_8_0003.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')], positions=[[np.float64(0.9986090868311966), np.float64(0.26601611741655384), np.float64(0.24565264312523877)], [np.float64(0.4202742292372096), np.float64(-0.5378797447581142), np.float64(-0.48610169536433384)], [np.float64(1.5420907940825435), np.float64(1.4776962849774407), np.float64(-0.21125385468766034)], [np.float64(1.084057085305652), np.float64(2.117473311078448), np.float64(-1.5217802174462214)], [np.float64(0.871834353221381), np.float64(3.42960064207624), np.float64(-1.3643610610004662)], [np.float64(1.9870910887512645), np.float64(2.0257467390704265), np.float64(-2.4825262662277967)], [np.float64(-0.03347902399749884), np.float64(1.632729177805033), np.float64(-1.9943100252608714)], [np.float64(1.6960902266028126), np.float64(-0.4734507406981796), np.float64(-1.8990778621294162)], [np.float64(2.4199256754206524), np.float64(2.126681007294445), np.float64(0.46511820164144957)], [np.float64(1.3006181525270442), np.float64(-0.10585611248327047), np.float64(1.4925455132485572)], [np.float64(1.0301843320177426), np.float64(-1.0212706817790227), np.float64(1.63976762410152)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1642764945472630600001_ketoenol_2_1_3_8_0003', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')])
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
            freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')])
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
