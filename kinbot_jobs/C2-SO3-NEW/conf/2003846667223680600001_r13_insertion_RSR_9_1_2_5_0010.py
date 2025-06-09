import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003846667223680600001_r13_insertion_RSR_9_1_2_5_0010'
logfile = 'conf/2003846667223680600001_r13_insertion_RSR_9_1_2_5_0010.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.31172306375951303), np.float64(1.3665637232357677), np.float64(-0.19748459363676266)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.39178298753025104), np.float64(-0.5573269881405859), np.float64(1.1374575469019914)], [np.float64(-0.32476240077624535), np.float64(-0.8571637249679758), np.float64(-0.953850925902607)], [np.float64(2.3019423409386883), np.float64(0.0), np.float64(0.0)], [np.float64(2.2626215687302556), np.float64(-0.5546069720511), np.float64(1.327702539495236)], [np.float64(2.2343751581971687), np.float64(-0.528006905292604), np.float64(-1.3366411512940415)], [np.float64(3.7131618046538075), np.float64(0.7712254494342097), np.float64(0.0)], [np.float64(1.5845252239542529), np.float64(1.8416416209488211), np.float64(0.09091160645567141)], [np.float64(-0.3382446940472973), np.float64(1.9505010082742), np.float64(-1.3344684856008868)], [np.float64(-0.6478842861792945), np.float64(2.186197904914114), np.float64(0.7213514992498922)], [np.float64(3.8859003654416844), np.float64(1.490075939373194), np.float64(-0.6219553944705318)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_RSR_9_1_2_5_0010', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
