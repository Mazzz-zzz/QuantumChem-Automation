import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003846667223680600001_r13_insertion_RSR_9_1_2_5_0008'
logfile = 'conf/2003846667223680600001_r13_insertion_RSR_9_1_2_5_0008.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.32768218671090404), np.float64(1.3691242349077306), np.float64(0.14761794007397344)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.3462632398461557), np.float64(-0.8254359986987884), np.float64(0.9780971999644165)], [np.float64(-0.35674047676571663), np.float64(-0.6002494054239218), np.float64(-1.123596342137111)], [np.float64(2.3019423407235613), np.float64(0.0), np.float64(0.0)], [np.float64(2.262738858141063), np.float64(-0.5707540441980841), np.float64(1.3208451672883876)], [np.float64(2.235972687879804), np.float64(-0.5172920247344476), np.float64(-1.3409038550223864)], [np.float64(3.7111603807082445), np.float64(0.7748764961010147), np.float64(0.0)], [np.float64(1.5917181983339617), np.float64(1.8360256107371207), np.float64(0.19795889348365595)], [np.float64(-0.5191754140111184), np.float64(2.1836557554755514), np.float64(-0.8189674241245066)], [np.float64(-0.5182141393246681), np.float64(1.961211548173182), np.float64(1.2621557425227852)], [np.float64(4.010195427823688), np.float64(1.263509430251196), np.float64(0.7779646735711896)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_RSR_9_1_2_5_0008', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
