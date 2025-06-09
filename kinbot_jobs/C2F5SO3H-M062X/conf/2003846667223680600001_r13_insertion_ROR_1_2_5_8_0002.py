import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/2003846667223680600001_r13_insertion_ROR_1_2_5_8_0002'
logfile = 'conf/2003846667223680600001_r13_insertion_ROR_1_2_5_8_0002.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.12890726382391104), np.float64(0.4741263570475751), np.float64(0.038335023543063)], [np.float64(1.8500496141418588), np.float64(-0.15535893441045157), np.float64(0.3087352324441736)], [np.float64(2.0066097410420234), np.float64(-0.5738284827070752), np.float64(1.5641745603276813)], [np.float64(2.0917265736205706), np.float64(-1.2116355786319335), np.float64(-0.46156021278210413)], [np.float64(2.607605739431365), np.float64(1.4825682586945645), np.float64(-0.17015559187847948)], [np.float64(2.780603555098246), np.float64(2.4979169763637517), np.float64(0.8040112556971417)], [np.float64(2.9793075263415854), np.float64(1.72534701358658), np.float64(-1.51820247739687)], [np.float64(0.8293158395228512), np.float64(1.7792684538033465), np.float64(-0.3297691726236704)], [np.float64(-0.2913086467959887), np.float64(0.1570819752513005), np.float64(1.3049788376936298)], [np.float64(-1.2585820271233488), np.float64(1.2504783940711943), np.float64(-0.21911293050055697)], [np.float64(-0.19593197196966064), np.float64(-0.4629922739460099), np.float64(-0.8922462633986185)], [np.float64(0.4256983205144068), np.float64(2.629165840877155), np.float64(-0.08254926112538959)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_ROR_1_2_5_8_0002', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
