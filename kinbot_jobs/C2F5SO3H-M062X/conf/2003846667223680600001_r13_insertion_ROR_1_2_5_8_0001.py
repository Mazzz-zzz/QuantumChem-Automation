import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/2003846667223680600001_r13_insertion_ROR_1_2_5_8_0001'
logfile = 'conf/2003846667223680600001_r13_insertion_ROR_1_2_5_8_0001.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.10149197692605635), np.float64(0.4727343099664558), np.float64(-0.00845244665785435)], [np.float64(1.8530999273158208), np.float64(-0.14960487124844846), np.float64(0.41333276074831937)], [np.float64(2.0280779091961225), np.float64(-0.43940148303472953), np.float64(1.7021913143290215)], [np.float64(2.0876243286664877), np.float64(-1.276996532418663), np.float64(-0.25109896694947514)], [np.float64(2.577256407702633), np.float64(1.4530482227762043), np.float64(-0.2136709447735873)], [np.float64(3.1344365508387453), np.float64(2.4222315977648345), np.float64(0.6581640062537402)], [np.float64(2.49422999973014), np.float64(1.7455930376214062), np.float64(-1.599981982677897)], [np.float64(0.8414368648930175), np.float64(1.8323239080261884), np.float64(0.131152108742143)], [np.float64(-0.42039709457221486), np.float64(-0.11548070827088655), np.float64(1.124499678618002)], [np.float64(-1.2148354843520275), np.float64(1.2681934194164086), np.float64(-0.27841178760693547)], [np.float64(0.00986499558235209), np.float64(-0.24908621299388567), np.float64(-1.110831659708161)], [np.float64(0.4068845719249781), np.float64(2.628583312395114), np.float64(-0.2202530803173153)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_ROR_1_2_5_8_0001', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')])
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
            freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')])
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
