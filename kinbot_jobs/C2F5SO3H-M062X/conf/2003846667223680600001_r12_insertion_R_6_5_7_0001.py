import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/2003846667223680600001_r12_insertion_R_6_5_7_0001'
logfile = 'conf/2003846667223680600001_r12_insertion_R_6_5_7_0001.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.8163379114227626), np.float64(0.7568527443885806), np.float64(-1.0578069768135372)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.3377672338299998), np.float64(0.44750245861580285), np.float64(1.2136714053287414)], [np.float64(-0.3107436158653372), np.float64(-1.29994923286388), np.float64(-0.07981153732102399)], [np.float64(2.032246175357208), np.float64(0.0), np.float64(0.0)], [np.float64(1.9092934433949584), np.float64(-0.48225968225756893), np.float64(1.4371078013781178)], [np.float64(3.472914203576468), np.float64(-0.28777348481011766), np.float64(0.5637792384959492)], [np.float64(2.047317349008509), np.float64(1.5963487514295778), np.float64(0.0)], [np.float64(-0.6681085479751724), np.float64(2.0652244164717777), np.float64(-0.9150018718867817)], [np.float64(-0.42909670524474014), np.float64(0.40893667702658676), np.float64(-2.2781625824048555)], [np.float64(-2.1082795330393016), np.float64(0.46561451259991177), np.float64(-0.9271835625516299)], [np.float64(1.2825665151946057), np.float64(1.9165715475883767), np.float64(0.49860157318462267)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r12_insertion_R_6_5_7_0001', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
