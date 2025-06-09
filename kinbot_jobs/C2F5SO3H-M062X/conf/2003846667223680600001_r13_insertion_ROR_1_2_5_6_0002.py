import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/2003846667223680600001_r13_insertion_ROR_1_2_5_6_0002'
logfile = 'conf/2003846667223680600001_r13_insertion_ROR_1_2_5_6_0002.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.18863268452564197), np.float64(0.556176948816444), np.float64(0.3394675177187386)], [np.float64(1.6895754723578704), np.float64(-0.5003281457152532), np.float64(-0.5173960604989754)], [np.float64(2.0560062305956945), np.float64(-1.6205131632347658), np.float64(0.1145503379508015)], [np.float64(1.4128041464501278), np.float64(-0.8799666596191401), np.float64(-1.7809222797054942)], [np.float64(2.5468622933824907), np.float64(1.0673658967064568), np.float64(-0.17244589433890195)], [np.float64(1.3044725244910547), np.float64(1.6766761297781962), np.float64(0.36219724997989194)], [np.float64(3.65754576948327), np.float64(1.3455758152607817), np.float64(0.6714288616125917)], [np.float64(2.777003739506561), np.float64(1.89428668003463), np.float64(-1.5027419110200064)], [np.float64(-0.8412075514748625), np.float64(1.5685830935353196), np.float64(0.8708183854307162)], [np.float64(-0.6269776421824365), np.float64(0.3209288265292624), np.float64(-0.8623588152708922)], [np.float64(-0.10256596957420212), np.float64(-0.4195251961206624), np.float64(1.195317171099567)], [np.float64(3.0736036714900754), np.float64(2.814918774028732), np.float64(-1.4605115629580356)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_ROR_1_2_5_6_0002', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
