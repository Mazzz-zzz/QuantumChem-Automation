import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = '2003846667223680600001_R_Addition_MultipleBond_5_2_3'
logfile = '2003846667223680600001_R_Addition_MultipleBond_5_2_3.log'

atom = [np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')]
geom = [[np.float64(-0.6652410411044953), np.float64(-1.3445371627975835), np.float64(0.2579001571523293)], [np.float64(0.1380562716905779), np.float64(-0.03444093623324739), np.float64(0.19780404986216163)], [np.float64(0.12375483769990084), np.float64(0.4462721164637698), np.float64(-1.1317541613590638)], [np.float64(-0.364081220634131), np.float64(0.882678251316057), np.float64(1.0068578344825765)], [np.float64(1.973721923868426), np.float64(-0.06862168891258594), np.float64(0.16531757380697654)], [np.float64(2.468077964166037), np.float64(-0.4173646338048505), np.float64(1.4388357967143854)], [np.float64(2.3728792860225676), np.float64(-0.7540121667107622), np.float64(-1.013189548838958)], [np.float64(2.1836461246444117), np.float64(1.4822881832204333), np.float64(-0.00305340452621527)], [np.float64(-0.13863541465921747), np.float64(-2.2436325418315906), np.float64(-0.5566952824679204)], [np.float64(-0.6453270185261084), np.float64(-1.80978515351932), np.float64(1.4975611008106804)], [np.float64(-1.9213075711189507), np.float64(-1.1060322829565885), np.float64(-0.10435604135021284)], [np.float64(2.3305301671263265), np.float64(1.8554656193955732), np.float64(-0.8852264919602243)]]
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
