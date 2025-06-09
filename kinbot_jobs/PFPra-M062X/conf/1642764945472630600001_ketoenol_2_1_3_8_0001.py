import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1642764945472630600001_ketoenol_2_1_3_8_0001'
logfile = 'conf/1642764945472630600001_ketoenol_2_1_3_8_0001.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')], positions=[[np.float64(1.5148976349823344), np.float64(0.2219484213642009), np.float64(0.1674101307232946)], [np.float64(1.6868644574844711), np.float64(-0.657258101011909), np.float64(-0.6773427796262076)], [np.float64(1.087672649569479), np.float64(1.5230772739845495), np.float64(-0.14379279802639494)], [np.float64(1.236750051294292), np.float64(2.099928944929524), np.float64(-1.551488413927187)], [np.float64(1.6908975148859455), np.float64(3.3581855676492807), np.float64(-1.5063468171349454)], [np.float64(2.1019958623677844), np.float64(1.443925329612803), np.float64(-2.305097124409554)], [np.float64(0.11219795811520158), np.float64(2.1561854935260674), np.float64(-2.2143353344671057)], [np.float64(0.07529368317116403), np.float64(-0.3270485873897483), np.float64(-1.637634672634044)], [np.float64(0.5902348955250412), np.float64(2.3055056896204125), np.float64(0.7448105233277906)], [np.float64(1.5441828672685698), np.float64(-0.11720796223590857), np.float64(1.4590585284505282)], [np.float64(1.6763084253357161), np.float64(-1.0697560700492723), np.float64(1.5484317577238251)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1642764945472630600001_ketoenol_2_1_3_8_0001', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
