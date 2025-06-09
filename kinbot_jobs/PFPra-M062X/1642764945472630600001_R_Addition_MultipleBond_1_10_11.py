import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = '1642764945472630600001_R_Addition_MultipleBond_1_10_11'
logfile = '1642764945472630600001_R_Addition_MultipleBond_1_10_11.log'

atom = [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')]
geom = [[np.float64(1.499783865998885), np.float64(0.029807852663741564), np.float64(-0.021051633673661158)], [np.float64(2.1720486784644657), np.float64(-0.9446937227045173), np.float64(-0.11806652655467977)], [np.float64(-0.04405051010671536), np.float64(-0.00030406330259774117), np.float64(-0.0003498167630017139)], [np.float64(-0.6304365482420239), np.float64(0.39912502599674443), np.float64(1.3713158718892677)], [np.float64(-1.9315108024890724), np.float64(0.15973088551833758), np.float64(1.399213529015833)], [np.float64(-0.031423363781201884), np.float64(-0.3201030302735508), np.float64(2.3141647362583497)], [np.float64(-0.41880475866467526), np.float64(1.6858030031304585), np.float64(1.6064535716055768)], [np.float64(-0.5260016771542027), np.float64(0.8447146714150303), np.float64(-0.9241564188830017)], [np.float64(-0.4471608401459555), np.float64(-1.2418169126969152), np.float64(-0.2698316755110111)], [np.float64(1.9641701955289992), np.float64(1.26934659184785), np.float64(0.09828710603391244)], [np.float64(3.2620359932703735), np.float64(0.7870627307636345), np.float64(0.057214065120324495)]]
mol = Atoms(symbols=atom, positions=geom)

kwargs = {'method': 'mp2', 'basis': '6-31G', 'nprocshared': 8, 'mem': '28GB', 'chk': '1642764945472630600001_R_Addition_MultipleBond_1_10_11', 'label': '1642764945472630600001_R_Addition_MultipleBond_1_10_11', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'guess': 'Mix,Always', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999', 'addsec': '1 2 F\n1 3 F\n1 10 F\n3 4 F\n3 8 F\n3 9 F\n4 5 F\n4 6 F\n4 7 F\n10 11 F\n1 10 11 F\n'}
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
