import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1642764945472630600001_r13_insertion_ROR_8_3_1_2_0003'
logfile = 'conf/1642764945472630600001_r13_insertion_ROR_8_3_1_2_0003.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')], positions=[[np.float64(2.4170802608451867), np.float64(1.1261016357254232), np.float64(-0.1261290628645351)], [np.float64(1.9955188075913006), np.float64(1.4860511658553381), np.float64(0.9733145634080465)], [np.float64(1.9668757001309078), np.float64(-0.20131738553356418), np.float64(-0.037635296590127605)], [np.float64(1.7494104978157625), np.float64(-0.8990360164836811), np.float64(1.304953856075245)], [np.float64(1.7833455393785238), np.float64(-2.229094059699357), np.float64(1.1591923705576244)], [np.float64(2.660561217788534), np.float64(-0.6192782647628681), np.float64(2.1986829928812996)], [np.float64(0.5748598054652828), np.float64(-0.633332422059116), np.float64(1.849607487438402)], [np.float64(0.2678395985375309), np.float64(1.730836048982621), np.float64(0.20875856654369404)], [np.float64(1.7507968291053702), np.float64(-0.9422366427785022), np.float64(-1.0640364392159236)], [np.float64(2.9450909987421), np.float64(1.847613158632319), np.float64(-1.1185388983965465)], [np.float64(2.7775557445995007), np.float64(2.7799757821213866), np.float64(-0.9302501398371782)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1642764945472630600001_r13_insertion_ROR_8_3_1_2_0003', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
