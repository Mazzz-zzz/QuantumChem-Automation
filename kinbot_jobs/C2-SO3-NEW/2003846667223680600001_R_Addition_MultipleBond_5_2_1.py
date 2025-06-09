import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = '2003846667223680600001_R_Addition_MultipleBond_5_2_1'
logfile = '2003846667223680600001_R_Addition_MultipleBond_5_2_1.log'

atom = [np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')]
geom = [[np.float64(-0.2427835053232784), np.float64(-0.0730523645495038), np.float64(1.4498226376464975)], [np.float64(-0.04866461464254333), np.float64(0.41221503719582764), np.float64(0.11786786981104999)], [np.float64(-0.4296614697410338), np.float64(-0.37740658474616995), np.float64(-0.9137304343518095)], [np.float64(-0.4193717900581747), np.float64(1.689987089811906), np.float64(-0.14198754132204963)], [np.float64(1.826235508830435), np.float64(0.24675858139037063), np.float64(0.32960859404150994)], [np.float64(2.3288767617935857), np.float64(0.7559507078791512), np.float64(1.5699860702739532)], [np.float64(2.1643411922377336), np.float64(-1.0479345546873198), np.float64(-0.15984252278079097)], [np.float64(2.1037536140559676), np.float64(1.3512106084463344), np.float64(-0.8030863749651332)], [np.float64(0.47382918283029835), np.float64(-1.139521744195143), np.float64(1.8433850201578428)], [np.float64(-0.041321312278430715), np.float64(0.882380016493268), np.float64(2.4031618771999943)], [np.float64(-1.5149701061777314), np.float64(-0.47465893707539186), np.float64(1.6724069781491586)], [np.float64(3.0057007210567126), np.float64(1.6934513461471539), np.float64(-0.9060485642380627)]]
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
