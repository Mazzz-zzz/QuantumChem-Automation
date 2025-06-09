import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = '1642764945472630600001_r12_insertion_R_5_4_3'
logfile = '1642764945472630600001_r12_insertion_R_5_4_3.log'

atom = [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')]
geom = [[np.float64(1.516946), np.float64(0.358), np.float64(0.113445)], [np.float64(2.045006), np.float64(0.332521), np.float64(1.172495)], [np.float64(-0.026655), np.float64(0.284348), np.float64(-0.216021)], [np.float64(-0.396325), np.float64(0.129637), np.float64(1.946732)], [np.float64(-1.619049), np.float64(0.129487), np.float64(0.809478)], [np.float64(-0.479453), np.float64(-0.908175), np.float64(2.452722)], [np.float64(-0.591847), np.float64(1.084989), np.float64(2.575122)], [np.float64(-0.505356), np.float64(1.332675), np.float64(-0.667677)], [np.float64(-0.382472), np.float64(-0.740144), np.float64(-0.795282)], [np.float64(2.203335), np.float64(0.459686), np.float64(-1.023712)], [np.float64(3.165368), np.float64(0.508379), np.float64(-0.855202)]]
mol = Atoms(symbols=atom, positions=geom)

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'chk': '1642764945472630600001_r12_insertion_R_5_4_3', 'label': '1642764945472630600001_r12_insertion_R_5_4_3', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999', 'addsec': '1 2 F\n1 3 F\n1 10 F\n3 4 F\n3 8 F\n3 9 F\n4 5 F\n4 6 F\n4 7 F\n10 11 F\n'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy() # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')])
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
        freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')])
        zpe = reader_gauss.read_zpe(logfile)
        db.write(mol, name=label, data={'energy': e,
                                         'frequencies': np.asarray(freq),
                                         'zpe': zpe, 'status': 'normal'})
    except RuntimeError:
        db.write(mol, name=label, data={'status': 'error'})

with open(logfile,'a') as f:
    f.write('done\n')
