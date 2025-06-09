import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1642764945472630600001_r13_insertion_ROR_8_3_1_2_0001'
logfile = 'conf/1642764945472630600001_r13_insertion_ROR_8_3_1_2_0001.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')], positions=[[np.float64(2.2532567110003376), np.float64(1.0573484004053881), np.float64(-0.21804759111346989)], [np.float64(1.595619118274241), np.float64(1.3372448734282092), np.float64(-1.2206566979372608)], [np.float64(1.434551276001814), np.float64(1.9730510374924752e-05), np.float64(0.21129381553750087)], [np.float64(1.8886717528026788), np.float64(-1.0153765248253546), np.float64(1.2598132658178387)], [np.float64(2.8765381000225965), np.float64(-1.796972369385892), np.float64(0.8073968515713361)], [np.float64(2.3411881133635655), np.float64(-0.4636142679681182), np.float64(2.354344845257915)], [np.float64(0.9285006907646349), np.float64(-1.8444870613822921), np.float64(1.6305730631851825)], [np.float64(0.38632252914737714), np.float64(2.3364096755368897), np.float64(-0.13963271099677552)], [np.float64(0.2669970703431555), np.float64(-0.18507821187242152), np.float64(-0.29040994725462665)], [np.float64(3.3736140774065673), np.float64(1.6052699868395064), np.float64(0.2603175994905711)], [np.float64(3.5436755608730324), np.float64(2.41551876871371), np.float64(-0.23707249355821172)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1642764945472630600001_r13_insertion_ROR_8_3_1_2_0001', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')])
    zpe = reader_gauss.read_zpe(logfile)
    db.write(mol, name=label, data={'energy': e, 'frequencies': np.asarray(freq),
                                     'zpe': zpe, 'status': 'normal'})

except RuntimeError:
    for i in range(3):
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
            if i == 2:
                db.write(mol, name=label, data={'status': 'error'})
            pass
        else:
            break

with open(logfile, 'a') as f:
    f.write('done\n')
