import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = '1642764945472630600001_intra_H_migration_2_11'
logfile = '1642764945472630600001_intra_H_migration_2_11.log'

atom = [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')]
geom = [[np.float64(1.41702), np.float64(0.235386), np.float64(-1.153225)], [np.float64(0.535192), np.float64(0.455707), np.float64(-1.917959)], [np.float64(1.524252), np.float64(-0.636408), np.float64(0.116899)], [np.float64(2.508299), np.float64(-1.78876), np.float64(-0.180746)], [np.float64(2.453266), np.float64(-2.742347), np.float64(0.734969)], [np.float64(2.268694), np.float64(-2.388753), np.float64(-1.341637)], [np.float64(3.772534), np.float64(-1.394149), np.float64(-0.220919)], [np.float64(1.930543), np.float64(0.098125), np.float64(1.16339)], [np.float64(0.330959), np.float64(-1.092715), np.float64(0.496783)], [np.float64(2.390813), np.float64(0.973691), np.float64(-1.675674)], [np.float64(1.426247), np.float64(1.116838), np.float64(-2.375045)]]
mol = Atoms(symbols=atom, positions=geom)

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'chk': '1642764945472630600001_intra_H_migration_2_11', 'label': '1642764945472630600001_intra_H_migration_2_11', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999', 'addsec': ''}
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
