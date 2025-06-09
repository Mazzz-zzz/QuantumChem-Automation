import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = '2003846667223680600001_R_Addition_MultipleBond_5_2_1'
logfile = '2003846667223680600001_R_Addition_MultipleBond_5_2_1.log'

atom = [np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')]
geom = [[np.float64(-0.0013594613971087575), np.float64(-1.4181125893119966), np.float64(0.2150230154442151)], [np.float64(0.030745428821209723), np.float64(0.008485377931872184), np.float64(0.12229442708341863)], [np.float64(-0.40062557710303276), np.float64(0.5584210214170094), np.float64(-1.044277196901765)], [np.float64(-0.4635681858938405), np.float64(0.7222606095088561), np.float64(1.1555476922917585)], [np.float64(1.8850990522003293), np.float64(-0.024331529266047616), np.float64(0.24365623812624407)], [np.float64(2.1921408401271996), np.float64(0.10753654497964073), np.float64(1.6123249316024522)], [np.float64(2.4942966310081), np.float64(-0.9967036164602595), np.float64(-0.5841066015678364)], [np.float64(2.02632181650217), np.float64(1.3744847864680816), np.float64(-0.4726371336480313)], [np.float64(0.25894169331866645), np.float64(-2.0348571950158707), np.float64(-0.950221909227333)], [np.float64(0.7786093043473478), np.float64(-2.013097532279437), np.float64(1.1347047761257834)], [np.float64(-1.2318295626423947), np.float64(-1.8637379790691115), np.float64(0.5454083945791613)], [np.float64(2.8998467470181963), np.float64(1.6825236553593883), np.float64(-0.7675629504950279)]]
mol = Atoms(symbols=atom, positions=geom)

kwargs = {'method': 'mp2', 'basis': '6-31G', 'nprocshared': 8, 'mem': '28GB', 'chk': '2003846667223680600001_R_Addition_MultipleBond_5_2_1', 'label': '2003846667223680600001_R_Addition_MultipleBond_5_2_1', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'guess': 'Mix,Always', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999', 'addsec': '1 2 F\n1 9 F\n1 10 F\n1 11 F\n2 3 F\n2 4 F\n2 5 F\n5 6 F\n5 7 F\n5 8 F\n8 12 F\n5 2 1 F\n'}
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
