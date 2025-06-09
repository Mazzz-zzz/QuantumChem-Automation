import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003846667223680600001_r12_insertion_R_6_5_7_0003'
logfile = 'conf/2003846667223680600001_r12_insertion_R_6_5_7_0003.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.8174775245024661), np.float64(-1.3064133057348097), np.float64(-0.11767471649580002)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.32583223608967876), np.float64(0.8191351932180242), np.float64(-1.0093232546961701)], [np.float64(-0.3123019984282574), np.float64(0.601445281752283), np.float64(1.1562566690318512)], [np.float64(2.0418452207807034), np.float64(0.0), np.float64(0.0)], [np.float64(1.9521805275866717), np.float64(-0.5144889962524691), np.float64(1.455281322545764)], [np.float64(3.5347191390454324), np.float64(-0.266603932464722), np.float64(0.5773745363975274)], [np.float64(2.0539661386427035), np.float64(1.621307463087795), np.float64(0.0)], [np.float64(-0.6437603260120839), np.float64(-1.8614724299141414), np.float64(-1.3112121664716798)], [np.float64(-0.4485049061078451), np.float64(-2.173720760368988), np.float64(0.8200656470137383)], [np.float64(-2.117080429644999), np.float64(-1.0445938239237373), np.float64(0.03841194642985904)], [np.float64(1.9724113397530276), np.float64(1.9354252972866601), np.float64(-0.909558517514008)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r12_insertion_R_6_5_7_0003', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
