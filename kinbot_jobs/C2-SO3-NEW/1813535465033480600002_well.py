import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = '1813535465033480600002_well'
logfile = '1813535465033480600002_well.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.709015), np.float64(0.280581), np.float64(1.336234)], [np.float64(-0.058467), np.float64(-0.051255), np.float64(-0.038113)], [np.float64(-0.519296), np.float64(0.799425), np.float64(-0.953941)], [np.float64(1.817262), np.float64(0.040839), np.float64(-0.046608)], [np.float64(2.282562), np.float64(-0.513068), np.float64(1.194661)], [np.float64(2.232011), np.float64(-0.422843), np.float64(-1.330877)], [np.float64(2.031849), np.float64(1.627007), np.float64(-0.036712)], [np.float64(-0.492209), np.float64(-0.685765), np.float64(2.209339)], [np.float64(-0.199297), np.float64(1.423189), np.float64(1.816388)], [np.float64(-2.016015), np.float64(0.439216), np.float64(1.178273)], [np.float64(2.066986), np.float64(1.957273), np.float64(0.870832)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'chk': '1813535465033480600002_well', 'label': '1813535465033480600002_well', 'Symm': 'None', 'mult': 2, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('C'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')])
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
            freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('C'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')])
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
