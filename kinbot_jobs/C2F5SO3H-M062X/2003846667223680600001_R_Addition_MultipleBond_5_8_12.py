import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = '2003846667223680600001_R_Addition_MultipleBond_5_8_12'
logfile = '2003846667223680600001_R_Addition_MultipleBond_5_8_12.log'

atom = [np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')]
geom = [[np.float64(-0.6674373907416731), np.float64(-1.3511311350594486), np.float64(0.31034521707104284)], [np.float64(0.01063200413195929), np.float64(0.020496052840800166), np.float64(0.08966837006934097)], [np.float64(-0.3211811073838944), np.float64(0.48052924011047005), np.float64(-1.123095827241754)], [np.float64(-0.3817820912002676), np.float64(0.8600029267887055), np.float64(1.0436627268612428)], [np.float64(1.852538548371996), np.float64(-0.03547500805151162), np.float64(0.13340079929900645)], [np.float64(2.216842405027271), np.float64(-0.6567224914183829), np.float64(1.3467240588268872)], [np.float64(2.3337967469338543), np.float64(-0.4829354668567132), np.float64(-1.1244128892565897)], [np.float64(2.1140164798608474), np.float64(1.5141586655383665), np.float64(0.1563986869134861)], [np.float64(-0.10324320747855016), np.float64(-2.2498958988330546), np.float64(-0.476421740429085)], [np.float64(-0.538234714195075), np.float64(-1.7222685151673265), np.float64(1.573728531319672)], [np.float64(-1.9541410738958243), np.float64(-1.2443619322341695), np.float64(0.010785996243890709)], [np.float64(2.8190023873916092), np.float64(1.4128354875707207), np.float64(-1.0317299270788023)]]
mol = Atoms(symbols=atom, positions=geom)

kwargs = {'method': 'mp2', 'basis': '6-31G', 'nprocshared': 8, 'mem': '28GB', 'chk': '2003846667223680600001_R_Addition_MultipleBond_5_8_12', 'label': '2003846667223680600001_R_Addition_MultipleBond_5_8_12', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'guess': 'Mix,Always', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999', 'addsec': '1 2 F\n1 9 F\n1 10 F\n1 11 F\n2 3 F\n2 4 F\n2 5 F\n5 6 F\n5 7 F\n5 8 F\n8 12 F\n5 8 12 F\n'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy() # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')])
    zpe = reader_gauss.read_zpe(logfile)
    db.write(mol, name=label, data={'energy': e,'frequencies': np.asarray(freq), 'zpe':zpe, 'status': 'normal'})
except RuntimeError:
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
        db.write(mol, name=label, data={'status': 'error'})

with open(logfile,'a') as f:
    f.write('done\n')
