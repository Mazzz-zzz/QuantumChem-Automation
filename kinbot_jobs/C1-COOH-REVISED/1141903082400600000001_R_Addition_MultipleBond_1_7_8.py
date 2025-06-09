import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs_C1-COOH-REVISED/kinbot.db')
label = '1141903082400600000001_R_Addition_MultipleBond_1_7_8'
logfile = '1141903082400600000001_R_Addition_MultipleBond_1_7_8.log'

atom = [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')]
geom = [[np.float64(1.4901159393949583), np.float64(0.04346839712130912), np.float64(0.00039576571297443407)], [np.float64(2.1843672954724753), np.float64(-0.9205421763851576), np.float64(0.0027268106518033124)], [np.float64(-0.05292537556776272), np.float64(-0.009382733459136598), np.float64(-4.827139671675611e-05)], [np.float64(-0.5288849796487848), np.float64(0.60560709717808), np.float64(1.0796043276572933)], [np.float64(-0.5280629540538556), np.float64(0.6004620122180359), np.float64(-1.0829846692343268)], [np.float64(-0.4617885829312962), np.float64(-1.2637953311386763), np.float64(0.002780877518278824)], [np.float64(1.9255083876576615), np.float64(1.2989397561284963), np.float64(-0.0021886131970612253)], [np.float64(3.2342064376188713), np.float64(0.8450914239608704), np.float64(-0.0007702286261078848)]]
mol = Atoms(symbols=atom, positions=geom)

kwargs = {'method': 'mp2', 'basis': '6-31G', 'nprocshared': 8, 'mem': '28GB', 'chk': '1141903082400600000001_R_Addition_MultipleBond_1_7_8', 'label': '1141903082400600000001_R_Addition_MultipleBond_1_7_8', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'guess': 'Mix,Always', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999', 'addsec': '1 2 F\n1 3 F\n1 7 F\n3 4 F\n3 5 F\n3 6 F\n7 8 F\n1 7 8 F\n'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy() # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')])
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
        freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')])
        zpe = reader_gauss.read_zpe(logfile)
        db.write(mol, name=label, data={'energy': e,
                                         'frequencies': np.asarray(freq),
                                         'zpe': zpe, 'status': 'normal'})
    except RuntimeError:
        db.write(mol, name=label, data={'status': 'error'})

with open(logfile,'a') as f:
    f.write('done\n')
