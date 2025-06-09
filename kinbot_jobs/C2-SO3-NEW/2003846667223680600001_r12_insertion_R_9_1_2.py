import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = '2003846667223680600001_r12_insertion_R_9_1_2'
logfile = '2003846667223680600001_r12_insertion_R_9_1_2.log'

atom = [np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')]
geom = [[np.float64(-1.311008), np.float64(0.181971), np.float64(1.420198)], [np.float64(0.130671), np.float64(0.452871), np.float64(-0.218705)], [np.float64(-0.309539), np.float64(-0.354555), np.float64(-1.065223)], [np.float64(-0.3077), np.float64(1.634202), np.float64(-0.55689)], [np.float64(1.667027), np.float64(0.253394), np.float64(0.589415)], [np.float64(1.620417), np.float64(0.854878), np.float64(1.907103)], [np.float64(2.30593), np.float64(-0.992348), np.float64(0.194)], [np.float64(2.498249), np.float64(1.305363), np.float64(-0.316487)], [np.float64(-0.061258), np.float64(-0.883484), np.float64(1.119073)], [np.float64(-1.114579), np.float64(0.569572), np.float64(2.496879)], [np.float64(-2.251196), np.float64(-0.407939), np.float64(1.154696)], [np.float64(3.183414), np.float64(0.984103), np.float64(-0.905768)]]
mol = Atoms(symbols=atom, positions=geom)

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'chk': '2003846667223680600001_r12_insertion_R_9_1_2', 'label': '2003846667223680600001_r12_insertion_R_9_1_2', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999', 'addsec': '1 2 F\n1 9 F\n1 10 F\n1 11 F\n2 3 F\n2 4 F\n2 5 F\n5 6 F\n5 7 F\n5 8 F\n8 12 F\n'}
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
