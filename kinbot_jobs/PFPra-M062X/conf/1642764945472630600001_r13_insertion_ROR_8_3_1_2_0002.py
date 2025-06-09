import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1642764945472630600001_r13_insertion_ROR_8_3_1_2_0002'
logfile = 'conf/1642764945472630600001_r13_insertion_ROR_8_3_1_2_0002.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')], positions=[[np.float64(2.341382988937301), np.float64(1.2193354176068063), np.float64(-0.09258758634569798)], [np.float64(1.87833624144045), np.float64(2.177395385513017), np.float64(0.5268983035410287)], [np.float64(1.9036185602248326), np.float64(-0.11484857230962411), np.float64(-0.06305982253938618)], [np.float64(1.631571641823153), np.float64(-0.8861139616079633), np.float64(1.228368890019981)], [np.float64(2.0920439009585943), np.float64(-2.139615176341351), np.float64(1.138078746401087)], [np.float64(2.209650598847894), np.float64(-0.3726880609533441), np.float64(2.281663879575397)], [np.float64(0.34668589348445833), np.float64(-1.0117975355962334), np.float64(1.5113661756949877)], [np.float64(0.4572938562314418), np.float64(1.356171695479543), np.float64(1.4941474601203373)], [np.float64(1.8202830827303191), np.float64(-0.789612465476342), np.float64(-1.15250894718738)], [np.float64(3.0712953728091255), np.float64(1.5258203762660567), np.float64(-1.1684808447465322)], [np.float64(3.136772862512429), np.float64(2.4822358974194345), np.float64(-1.2859662545338226)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1642764945472630600001_r13_insertion_ROR_8_3_1_2_0002', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
