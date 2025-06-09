import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFMS-M062X/kinbot.db')
label = 'conf/1502984803620600000001_r13_insertion_ROR_2_1_5_8_0003'
logfile = 'conf/1502984803620600000001_r13_insertion_ROR_2_1_5_8_0003.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('H')], positions=[[np.float64(1.6193000151100927), np.float64(0.11846837316302368), np.float64(-0.21776848739649)], [np.float64(-0.28657537765481295), np.float64(0.46269903685022673), np.float64(0.6607462698992885)], [np.float64(1.8715704787224006), np.float64(-0.7805360567926571), np.float64(0.6243658828866668)], [np.float64(1.0809079355642763), np.float64(-0.373156112915869), np.float64(-1.23869149538963)], [np.float64(2.130109771240499), np.float64(1.9887398001634256), np.float64(-0.04917077600780646)], [np.float64(2.946748573832106), np.float64(1.9124542010136072), np.float64(1.1123882003697523)], [np.float64(2.731742966167644), np.float64(2.1662637062974675), np.float64(-1.3216673064456246)], [np.float64(0.7581407622195802), np.float64(2.41119639406414), np.float64(0.1266272131194948)], [np.float64(-0.37159912520178406), np.float64(1.4215636581566362), np.float64(0.6807484989643486)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1502984803620600000001_r13_insertion_ROR_2_1_5_8_0003', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('H')])
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
            freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('H')])
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
