import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/2003846667223680600001_r13_insertion_ROR_1_2_5_6_0001'
logfile = 'conf/2003846667223680600001_r13_insertion_ROR_1_2_5_6_0001.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.17999806421472675), np.float64(0.5275444250600493), np.float64(0.4010614812729051)], [np.float64(1.6549407956204005), np.float64(-0.4738029863867939), np.float64(-0.6031231773229491)], [np.float64(2.0133156509820798), np.float64(-1.635260927353051), np.float64(-0.045426899442353)], [np.float64(1.3754986796393724), np.float64(-0.7685537595518256), np.float64(-1.888525978109167)], [np.float64(2.4983691701791457), np.float64(1.0842680665696531), np.float64(-0.1876245708618331)], [np.float64(1.1899336760772634), np.float64(1.744227383351674), np.float64(0.042776921036809364)], [np.float64(3.4057020250996377), np.float64(1.3704748651578407), np.float64(0.8697192259783422)], [np.float64(3.0281106902080785), np.float64(1.8504515798631767), np.float64(-1.4677758529427531)], [np.float64(-0.840327488765456), np.float64(1.5486139493371567), np.float64(0.9055770716004488)], [np.float64(-0.7534840376541337), np.float64(0.10865089269155159), np.float64(-0.6886708539504733)], [np.float64(0.11547929540730181), np.float64(-0.3238115187898169), np.float64(1.3390204200363893)], [np.float64(3.2509496074210404), np.float64(2.791377030050386), np.float64(-1.4196047872953654)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_ROR_1_2_5_6_0001', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
