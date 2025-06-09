import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003846667223680600001_r12_insertion_R_9_1_10_0011'
logfile = 'conf/2003846667223680600001_r12_insertion_R_9_1_10_0011.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.3548439174837453), np.float64(-1.3350149912357663), np.float64(0.2115826938557025)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.23457001113567705), np.float64(0.5708161413115981), np.float64(-1.163682960364353)], [np.float64(-0.28539787276075845), np.float64(0.8914332932978193), np.float64(0.9390086685497493)], [np.float64(2.4025295115163035), np.float64(0.0), np.float64(0.0)], [np.float64(3.143760186521744), np.float64(-0.47868820906151516), np.float64(1.1388994942549286)], [np.float64(2.394138318586586), np.float64(-0.39096465671985314), np.float64(-1.376513325098325)], [np.float64(2.944521888981878), np.float64(1.5668408304323937), np.float64(0.0)], [np.float64(-0.5556748958688006), np.float64(-1.861992962506793), np.float64(1.3549060301119205)], [np.float64(1.6977450993030545), np.float64(-1.6678858873129006), np.float64(0.5206064851079532)], [np.float64(-0.3865566850513199), np.float64(-2.2302103217269886), np.float64(-0.6933356109558916)], [np.float64(3.196177815032352), np.float64(1.9612933188000823), np.float64(0.8448802820581127)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r12_insertion_R_9_1_10_0011', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
