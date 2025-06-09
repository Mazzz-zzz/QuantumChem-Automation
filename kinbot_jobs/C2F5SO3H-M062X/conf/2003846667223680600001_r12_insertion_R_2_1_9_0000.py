import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/2003846667223680600001_r12_insertion_R_2_1_9_0000'
logfile = 'conf/2003846667223680600001_r12_insertion_R_2_1_9_0000.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.1651917958952915), np.float64(-0.8502582436659802), np.float64(1.2934476709584857)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.6323905759912258), np.float64(-0.5298493539517694), np.float64(-1.0229825381527187)], [np.float64(-0.5519953835539504), np.float64(1.181800222774063), np.float64(0.2682070677019961)], [np.float64(1.8523257270412783), np.float64(0.0), np.float64(0.0)], [np.float64(2.0121393787351645), np.float64(-0.2460587517649863), np.float64(1.4287764781354437)], [np.float64(2.7102236560914137), np.float64(-0.2926055285124591), np.float64(-1.0996296455900196)], [np.float64(1.9367780107278365), np.float64(1.6208074499489828), np.float64(0.0)], [np.float64(1.2373360044828254), np.float64(-1.8173544407516709), np.float64(-0.07837418363631463)], [np.float64(-0.2867554072692341), np.float64(-0.25419345476516036), np.float64(2.395683888988154)], [np.float64(-0.6365224274065951), np.float64(-2.006150110769882), np.float64(1.334456439182039)], [np.float64(1.0352860579532597), np.float64(1.9576579498945832), np.float64(-0.0549575582889178)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r12_insertion_R_2_1_9_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
