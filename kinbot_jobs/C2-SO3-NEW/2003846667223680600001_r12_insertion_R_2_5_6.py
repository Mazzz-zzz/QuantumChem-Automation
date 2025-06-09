import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = '2003846667223680600001_r12_insertion_R_2_5_6'
logfile = '2003846667223680600001_r12_insertion_R_2_5_6.log'

atom = [np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')]
geom = [[np.float64(-0.678518), np.float64(-0.161518), np.float64(1.406397)], [np.float64(0.176937), np.float64(0.434664), np.float64(0.218633)], [np.float64(-0.569985), np.float64(0.15409), np.float64(-0.914281)], [np.float64(0.040871), np.float64(1.795061), np.float64(0.177716)], [np.float64(1.770461), np.float64(-0.039601), np.float64(0.061686)], [np.float64(1.428292), np.float64(0.856827), np.float64(1.584615)], [np.float64(2.112051), np.float64(-1.274734), np.float64(-0.317816)], [np.float64(2.412553), np.float64(0.965173), np.float64(-0.914289)], [np.float64(-0.105948), np.float64(-1.188844), np.float64(1.993588)], [np.float64(-0.940559), np.float64(0.739118), np.float64(2.352423)], [np.float64(-1.862228), np.float64(-0.600303), np.float64(0.985643)], [np.float64(2.266497), np.float64(1.918101), np.float64(-0.816021)]]
mol = Atoms(symbols=atom, positions=geom)

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'chk': '2003846667223680600001_r12_insertion_R_2_5_6', 'label': '2003846667223680600001_r12_insertion_R_2_5_6', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999', 'addsec': '1 2 F\n1 9 F\n1 10 F\n1 11 F\n2 3 F\n2 4 F\n2 5 F\n5 6 F\n5 7 F\n5 8 F\n8 12 F\n'}
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
