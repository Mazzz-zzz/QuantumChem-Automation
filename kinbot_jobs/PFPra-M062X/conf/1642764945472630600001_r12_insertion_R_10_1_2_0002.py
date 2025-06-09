import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1642764945472630600001_r12_insertion_R_10_1_2_0002'
logfile = 'conf/1642764945472630600001_r12_insertion_R_10_1_2_0002.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')], positions=[[np.float64(1.392671557125728), np.float64(0.0), np.float64(0.0)], [np.float64(0.9721007103857865), np.float64(-0.4258595939616439), np.float64(-1.3114076096867342)], [np.float64(1.9225634060883459), np.float64(1.4195027500417103), np.float64(0.0)], [np.float64(3.3161247532027183), np.float64(1.5399657306225543), np.float64(-0.6391469940118273)], [np.float64(3.6934222147409264), np.float64(2.8105231300390905), np.float64(-0.6599016836677337)], [np.float64(4.198782592842956), np.float64(0.8422393423558088), np.float64(0.05727279053831924)], [np.float64(3.2897110106818905), np.float64(1.0813013845242574), np.float64(-1.8851039505020046)], [np.float64(1.0830776095772792), np.float64(2.267812790527875), np.float64(-0.6704375728407094)], [np.float64(1.981501339876125), np.float64(1.8711534485995815), np.float64(1.2608545819590036)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.3859987865548614), np.float64(0.8909976901599651), np.float64(-0.19626997183415895)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1642764945472630600001_r12_insertion_R_10_1_2_0002', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
