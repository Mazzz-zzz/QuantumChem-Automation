import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003846667223680600001_r13_insertion_RSR_9_1_2_5_0002'
logfile = 'conf/2003846667223680600001_r13_insertion_RSR_9_1_2_5_0002.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.2368513618508327), np.float64(1.0914352228759758), np.float64(0.8696771981436993)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.3278132524909347), np.float64(-1.1986712562046347), np.float64(0.4622149312290954)], [np.float64(-0.397377203299528), np.float64(0.1848634401966681), np.float64(-1.2481781615933272)], [np.float64(2.301942340704693), np.float64(0.0), np.float64(0.0)], [np.float64(2.3418751576347896), np.float64(-0.8990005079935302), np.float64(1.1234467075110424)], [np.float64(2.214879572398059), np.float64(-0.35097863252206385), np.float64(-1.392551706651041)], [np.float64(3.681572374302226), np.float64(0.8264079130167308), np.float64(0.0)], [np.float64(1.648896331175713), np.float64(1.679488662199079), np.float64(0.8169729751883005)], [np.float64(-0.6650610230325472), np.float64(2.2220956672417844), np.float64(0.4541510668557211)], [np.float64(-0.30062496822885343), np.float64(0.9196125896854089), np.float64(2.1327980294239066)], [np.float64(3.761803458957658), np.float64(1.3134910680459002), np.float64(0.8304975075771406)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_RSR_9_1_2_5_0002', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
