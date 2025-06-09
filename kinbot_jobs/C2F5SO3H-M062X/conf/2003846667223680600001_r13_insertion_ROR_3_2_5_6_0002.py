import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_0002'
logfile = 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_0002.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(1.8927158918378788), np.float64(-0.9979506326723011), np.float64(-1.1799408061311638)], [np.float64(2.1541780033343243), np.float64(-0.04068827639881862), np.float64(-0.04155898266728614)], [np.float64(-0.3217749828342075), np.float64(0.527677182566529), np.float64(0.27086664847403136)], [np.float64(2.5387913754597187), np.float64(-0.61093987370377), np.float64(1.0825567646839496)], [np.float64(1.914641039587028), np.float64(1.6180994194982925), np.float64(-0.057097649968216584)], [np.float64(0.49741110657997567), np.float64(2.0433765632653427), np.float64(0.11888212415863934)], [np.float64(2.7928704055934435), np.float64(2.3951934306434), np.float64(0.7304372790819269)], [np.float64(2.111028596040482), np.float64(2.0542579511469055), np.float64(-1.5339050135545311)], [np.float64(1.2888466727597003), np.float64(-0.44355761934488297), np.float64(-2.218673852711377)], [np.float64(3.020916825908436), np.float64(-1.5270011961232268), np.float64(-1.6761004957521362)], [np.float64(1.1429318917408575), np.float64(-2.0381597057316307), np.float64(-0.8493518305882685)], [np.float64(2.9775251739923627), np.float64(2.2889197568541615), np.float64(-1.9001331850255676)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_0002', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
