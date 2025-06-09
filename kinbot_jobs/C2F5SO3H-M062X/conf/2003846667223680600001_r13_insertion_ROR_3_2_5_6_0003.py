import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_0003'
logfile = 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_0003.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(1.9848604246629569), np.float64(-1.0428073901729307), np.float64(-1.1932186581191542)], [np.float64(2.0291486604413587), np.float64(-0.10476218182038431), np.float64(-0.010533757605789968)], [np.float64(-0.3534894599768705), np.float64(0.7615471656437), np.float64(0.3409695921504018)], [np.float64(1.9693867022581864), np.float64(-0.6886283236718628), np.float64(1.1694241844695707)], [np.float64(1.9774406316056674), np.float64(1.5691024989749849), np.float64(-0.07912431351806325)], [np.float64(0.6772031306547955), np.float64(2.1503844613949727), np.float64(0.35890518021925616)], [np.float64(3.0352182267619088), np.float64(2.2925002186990966), np.float64(0.5151649871390783)], [np.float64(2.015473069950174), np.float64(1.9528604701442716), np.float64(-1.582801964294049)], [np.float64(1.3839720797234292), np.float64(-0.5406320603745843), np.float64(-2.259863323559019)], [np.float64(3.2049953020432245), np.float64(-1.3990285406905822), np.float64(-1.621344444449433)], [np.float64(1.3619335129411523), np.float64(-2.1834708270318286), np.float64(-0.9395338544173649)], [np.float64(2.7239397189340173), np.float64(2.5021615089051488), np.float64(-1.9520626280154338)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_0003', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
