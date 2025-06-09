import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1642764945472630600001_r12_insertion_R_3_1_2_0001'
logfile = 'conf/1642764945472630600001_r12_insertion_R_3_1_2_0001.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')], positions=[[np.float64(1.7748364674566501), np.float64(0.0), np.float64(0.0)], [np.float64(1.2662056190446689), np.float64(-0.40292262591733613), np.float64(-1.0881683961398552)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.299977622500595), np.float64(-1.127745089241568), np.float64(1.023009998502663)], [np.float64(-1.6146452810143177), np.float64(-1.2509545138425675), np.float64(1.1499068262468484)], [np.float64(0.19991130706731752), np.float64(-2.2813817754431343), np.float64(0.6097064718514696)], [np.float64(0.20197494621501166), np.float64(-0.8345236741059505), np.float64(2.2089873085835388)], [np.float64(-0.22520944356906725), np.float64(1.2110869675225704), np.float64(0.5218597124240336)], [np.float64(-0.9442015685154559), np.float64(-0.08077787575609993), np.float64(-0.9685652007264586)], [np.float64(3.0185931931201186), np.float64(0.37299967508281706), np.float64(0.0)], [np.float64(3.5213701535520743), np.float64(-0.18795103347590802), np.float64(0.6255617578131417)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1642764945472630600001_r12_insertion_R_3_1_2_0001', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
