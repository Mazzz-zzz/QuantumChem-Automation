import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/2003846667223680600001_r12_insertion_R_5_2_3_0002'
logfile = 'conf/2003846667223680600001_r12_insertion_R_5_2_3_0002.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.4600690176176215), np.float64(-2.2132759167057094), np.float64(-1.1199277198506437)], [np.float64(0.48537065608683855), np.float64(-1.737756657233638), np.float64(-0.0025363136644595157)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(0.027648431233864804), np.float64(-2.1604468952061655), np.float64(1.124454083094702)], [np.float64(1.7590147426676102), np.float64(0.0), np.float64(0.0)], [np.float64(2.2035797001031656), np.float64(-0.37634929890803465), np.float64(1.2950563317654384)], [np.float64(2.273295186636771), np.float64(-0.3174477576667001), np.float64(-1.2742962388401946)], [np.float64(1.8216838829835256), np.float64(1.5810943226028813), np.float64(0.0)], [np.float64(-0.23407511594506555), np.float64(-1.5626385696928333), np.float64(-2.243911204216789)], [np.float64(-0.2030028904683696), np.float64(-3.507279894490586), np.float64(-1.3013325428554339)], [np.float64(-1.7400077439154027), np.float64(-2.0768854528642704), np.float64(-0.7924807562163285)], [np.float64(1.7160287558883058), np.float64(1.9061298585340947), np.float64(0.904167633880135)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r12_insertion_R_5_2_3_0002', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
