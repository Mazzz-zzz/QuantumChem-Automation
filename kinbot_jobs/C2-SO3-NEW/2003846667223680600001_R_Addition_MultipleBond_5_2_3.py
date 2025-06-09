import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = '2003846667223680600001_R_Addition_MultipleBond_5_2_3'
logfile = '2003846667223680600001_R_Addition_MultipleBond_5_2_3.log'

atom = [np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')]
geom = [[np.float64(-0.8344546637851047), np.float64(0.3466491138275256), np.float64(1.3157451822680053)], [np.float64(-0.05666480813126037), np.float64(0.07262096343454785), np.float64(0.007101932172826935)], [np.float64(-0.09724501559156284), np.float64(-1.3176515157618323), np.float64(-0.24434715480852967)], [np.float64(-0.5631338320795923), np.float64(0.7115583373442401), np.float64(-1.0317198043216138)], [np.float64(1.8123290530389722), np.float64(0.024664065458142592), np.float64(-0.03199196457008742)], [np.float64(2.3012757464841864), np.float64(-0.9472817260751112), np.float64(0.9071803358097684)], [np.float64(2.2035802306491683), np.float64(-0.019567191023941766), np.float64(-1.4058390965507144)], [np.float64(1.9952789045413426), np.float64(1.500554712824273), np.float64(0.5614572936820975)], [np.float64(-0.21552219747369936), np.float64(-0.20549037687947214), np.float64(2.345807905951839)], [np.float64(-0.9285288782509596), np.float64(1.6705251033685073), np.float64(1.5137010629052265)], [np.float64(-2.055884257587766), np.float64(-0.16407237367520539), np.float64(1.2132213156575395)], [np.float64(2.8744421666900624), np.float64(1.889423278882834), np.float64(0.650801477353708)]]
mol = Atoms(symbols=atom, positions=geom)

kwargs = {'method': 'mp2', 'basis': '6-31G', 'nprocshared': 8, 'mem': '28GB', 'chk': '2003846667223680600001_R_Addition_MultipleBond_5_2_3', 'label': '2003846667223680600001_R_Addition_MultipleBond_5_2_3', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'guess': 'Mix,Always', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999', 'addsec': '1 2 F\n1 9 F\n1 10 F\n1 11 F\n2 3 F\n2 4 F\n2 5 F\n5 6 F\n5 7 F\n5 8 F\n8 12 F\n5 2 3 F\n'}
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
