import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = '1642764945472630600001_R_Addition_MultipleBond_1_3_4'
logfile = '1642764945472630600001_R_Addition_MultipleBond_1_3_4.log'

atom = [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')]
geom = [[np.float64(1.6592328192404806), np.float64(0.06298394019563207), np.float64(-0.05858113636549813)], [np.float64(2.302974853277485), np.float64(-0.773417930903184), np.float64(0.4860772956448943)], [np.float64(0.15199232577062208), np.float64(-0.029152693615608197), np.float64(-0.24496177661498247)], [np.float64(-0.131041399982058), np.float64(0.3627812756168323), np.float64(1.8495806354366315)], [np.float64(-1.3613448973033169), np.float64(0.49268545054312357), np.float64(1.5730429403532715)], [np.float64(0.35305131382668664), np.float64(-0.8064076860031117), np.float64(2.037632359277556)], [np.float64(0.6308933180536022), np.float64(1.3628031135581082), np.float64(1.7034053271929743)], [np.float64(-0.5968195450751816), np.float64(1.022096936542947), np.float64(-0.4562288869302618)], [np.float64(-0.4522280428230579), np.float64(-1.1560308987797643), np.float64(-0.01909614275643399)], [np.float64(2.1110218169586137), np.float64(1.2493377902404539), np.float64(-0.47952810132653734)], [np.float64(3.0690533412927197), np.float64(1.3359634469287835), np.float64(-0.330215397099071)]]
mol = Atoms(symbols=atom, positions=geom)

kwargs = {'method': 'mp2', 'basis': '6-31G', 'nprocshared': 8, 'mem': '28GB', 'chk': '1642764945472630600001_R_Addition_MultipleBond_1_3_4', 'label': '1642764945472630600001_R_Addition_MultipleBond_1_3_4', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'guess': 'Mix,Always', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999', 'addsec': '1 2 F\n1 3 F\n1 10 F\n3 4 F\n3 8 F\n3 9 F\n4 5 F\n4 6 F\n4 7 F\n10 11 F\n1 3 4 F\n'}
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
