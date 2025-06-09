import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = '2003846667223680600001_Intra_Diels_alder_R_6_7'
logfile = '2003846667223680600001_Intra_Diels_alder_R_6_7.log'

atom = [np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')]
geom = [[np.float64(-0.938373), np.float64(0.081667), np.float64(1.25621)], [np.float64(-0.076634), np.float64(0.230366), np.float64(-0.042179)], [np.float64(-0.458098), np.float64(-0.669215), np.float64(-0.959259)], [np.float64(-0.445175), np.float64(1.362937), np.float64(-0.650879)], [np.float64(1.741902), np.float64(0.137262), np.float64(0.166085)], [np.float64(2.40244), np.float64(-1.032346), np.float64(-0.199699)], [np.float64(2.167885), np.float64(-0.27358), np.float64(1.415917)], [np.float64(2.489342), np.float64(1.410539), np.float64(-0.323059)], [np.float64(-0.341849), np.float64(-0.6566), np.float64(2.171082)], [np.float64(-1.180148), np.float64(1.269635), np.float64(1.820742)], [np.float64(-2.123883), np.float64(-0.459714), np.float64(1.027375)], [np.float64(2.813024), np.float64(2.197079), np.float64(0.135948)]]
mol = Atoms(symbols=atom, positions=geom)

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'chk': '2003846667223680600001_Intra_Diels_alder_R_6_7', 'label': '2003846667223680600001_Intra_Diels_alder_R_6_7', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999', 'addsec': ''}
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
