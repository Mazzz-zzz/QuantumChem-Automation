import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs_C1-COOH-REVISED/kinbot.db')
label = '1141903082400600000001_R_Addition_MultipleBond_1_3_4'
logfile = '1141903082400600000001_R_Addition_MultipleBond_1_3_4.log'

atom = [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')]
geom = [[np.float64(1.5871509228126184), np.float64(-0.018585785515907838), np.float64(0.015109866499504677)], [np.float64(2.225311388342583), np.float64(-0.9500594895535215), np.float64(0.3928914201743796)], [np.float64(0.05921216967703977), np.float64(-0.03804274543675393), np.float64(-0.11410344518897494)], [np.float64(-0.05875952595074424), np.float64(0.42906164129266267), np.float64(1.2144966459096076)], [np.float64(-0.5530656394292754), np.float64(0.8405654638666057), np.float64(-0.892447597812312)], [np.float64(-0.5172249960900278), np.float64(-1.2135614140023607), np.float64(-0.1685624495269098)], [np.float64(2.042745768159913), np.float64(1.199185542683392), np.float64(-0.27229857587054784)], [np.float64(2.990352450877179), np.float64(1.2972403554930838), np.float64(-0.10536200342090958)]]
mol = Atoms(symbols=atom, positions=geom)

kwargs = {'method': 'mp2', 'basis': '6-31G', 'nprocshared': 8, 'mem': '28GB', 'chk': '1141903082400600000001_R_Addition_MultipleBond_1_3_4', 'label': '1141903082400600000001_R_Addition_MultipleBond_1_3_4', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'guess': 'Mix,Always', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999', 'addsec': '1 2 F\n1 3 F\n1 7 F\n3 4 F\n3 5 F\n3 6 F\n7 8 F\n1 3 4 F\n'}
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
