import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003846667223680600001_r12_insertion_R_2_5_6_0010'
logfile = 'conf/2003846667223680600001_r12_insertion_R_2_5_6_0010.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.5795058344721253), np.float64(-1.4287697543383098), np.float64(-0.0814385944857117)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.5162523893030317), np.float64(0.7815101625877785), np.float64(-0.9335770656602561)], [np.float64(-0.37911032120491456), np.float64(0.5936534297132029), np.float64(1.1479207837112326)], [np.float64(1.9277442911526383), np.float64(0.0), np.float64(0.0)], [np.float64(1.2891451615545313), np.float64(0.8534311973669014), np.float64(2.4572561518577087)], [np.float64(2.3464875819551043), np.float64(-0.26916926198977625), np.float64(-1.3649822672726204)], [np.float64(2.1598311866439004), np.float64(1.596814609495051), np.float64(0.0)], [np.float64(-0.5033645734539107), np.float64(-1.955668338127273), np.float64(-1.292208607830635)], [np.float64(0.046286514234894285), np.float64(-2.2864613499528468), np.float64(0.7240304802820643)], [np.float64(-1.8600908237570757), np.float64(-1.4997361229786983), np.float64(0.26450816824244844)], [np.float64(1.7938660766770689), np.float64(2.078797044448713), np.float64(-0.7742936177045859)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r12_insertion_R_2_5_6_0010', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
