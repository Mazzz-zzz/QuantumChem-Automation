import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = '2003846667223680600001_R_Addition_MultipleBond_5_8_12'
logfile = '2003846667223680600001_R_Addition_MultipleBond_5_8_12.log'

atom = [np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')]
geom = [[np.float64(-0.7787099235973701), np.float64(0.24470739749613893), np.float64(1.3324912696203528)], [np.float64(-0.11612672240001104), np.float64(-0.05231650731957456), np.float64(-0.04406902235129688)], [np.float64(-0.3939241283455557), np.float64(-1.306190784762722), np.float64(-0.3995599257149657)], [np.float64(-0.5680757762025415), np.float64(0.8084302539635302), np.float64(-0.9549030049083151)], [np.float64(1.7570910357373632), np.float64(0.07936796064818866), np.float64(-0.06914914888286354)], [np.float64(2.2827566795372984), np.float64(-0.3125881941981815), np.float64(1.2091740779453308)], [np.float64(2.179926028288807), np.float64(-0.5334457316793074), np.float64(-1.2865378187483885)], [np.float64(1.9000030834984944), np.float64(1.6727597412606359), np.float64(-0.12162247553038999)], [np.float64(-0.5336722689366651), np.float64(-0.7432515129154549), np.float64(2.173345333561133)], [np.float64(-0.283459572141704), np.float64(1.3863540908915444), np.float64(1.8297682145799767)], [np.float64(-2.087400929429268), np.float64(0.37510516733042065), np.float64(1.1631132787923923)], [np.float64(2.6460765042699794), np.float64(1.6442642244272385), np.float64(1.0450342231611527)]]
mol = Atoms(symbols=atom, positions=geom)

kwargs = {'method': 'mp2', 'basis': '6-31G', 'nprocshared': 8, 'mem': '28GB', 'chk': '2003846667223680600001_R_Addition_MultipleBond_5_8_12', 'label': '2003846667223680600001_R_Addition_MultipleBond_5_8_12', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'guess': 'Mix,Always', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999', 'addsec': '1 2 F\n1 9 F\n1 10 F\n1 11 F\n2 3 F\n2 4 F\n2 5 F\n5 6 F\n5 7 F\n5 8 F\n8 12 F\n5 8 12 F\n'}
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
