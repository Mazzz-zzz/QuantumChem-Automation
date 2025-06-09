import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003846667223680600001_r12_insertion_R_9_1_10_0008'
logfile = 'conf/2003846667223680600001_r12_insertion_R_9_1_10_0008.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.36194579235433433), np.float64(-1.3429283528330833), np.float64(0.1359596752477286)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.2587332076350346), np.float64(0.6369399434954963), np.float64(-1.1235553555688418)], [np.float64(-0.26685808535879907), np.float64(0.8375301788048427), np.float64(0.9925584661696031)], [np.float64(2.4025294927179206), np.float64(0.0), np.float64(0.0)], [np.float64(2.9016925325061576), np.float64(-0.40432268581883885), np.float64(1.2895797576027206)], [np.float64(2.672395400378225), np.float64(-0.41832161433335585), np.float64(-1.3416003895912694)], [np.float64(2.925733281372574), np.float64(1.5732142586358746), np.float64(0.0)], [np.float64(-0.4879410857249968), np.float64(-1.9506689596149398), np.float64(1.2495141310870637)], [np.float64(1.702048460199939), np.float64(-1.740082325498789), np.float64(0.17616801922446423)], [np.float64(-0.4839882588223206), np.float64(-2.1661117443475977), np.float64(-0.8277477881394973)], [np.float64(3.0266171539419116), np.float64(2.023251409107442), np.float64(0.8485485757402287)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r12_insertion_R_9_1_10_0008', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
