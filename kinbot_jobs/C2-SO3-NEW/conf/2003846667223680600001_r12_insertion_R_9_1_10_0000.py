import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003846667223680600001_r12_insertion_R_9_1_10_0000'
logfile = 'conf/2003846667223680600001_r12_insertion_R_9_1_10_0000.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.20856227664793164), np.float64(-1.3817473304221015), np.float64(0.014914493783775115)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.29580650745870235), np.float64(0.6442949156052786), np.float64(-1.1101326825282067)], [np.float64(-0.3412973637840973), np.float64(0.6640606828524539), np.float64(1.0956193980705882)], [np.float64(2.40252949267933), np.float64(0.0), np.float64(0.0)], [np.float64(3.0546168175290482), np.float64(-0.4631685823137329), np.float64(1.1982960857287424)], [np.float64(2.6129542698595727), np.float64(-0.35409361466125056), np.float64(-1.3704201217797314)], [np.float64(2.8439670773177785), np.float64(1.5980857817243643), np.float64(0.0)], [np.float64(-0.46999830316743385), np.float64(-2.0202829015809756), np.float64(1.0868988748675232)], [np.float64(1.8426847010747154), np.float64(-1.7827535653312927), np.float64(0.2407465091683578)], [np.float64(-0.30002830768962807), np.float64(-2.0524396577801456), np.float64(-1.0635395393036486)], [np.float64(3.5740073131462857), np.float64(1.70346897708279), np.float64(-0.6234431115960024)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r12_insertion_R_9_1_10_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
