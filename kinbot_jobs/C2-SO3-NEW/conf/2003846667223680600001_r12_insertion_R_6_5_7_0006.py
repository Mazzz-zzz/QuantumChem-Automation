import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003846667223680600001_r12_insertion_R_6_5_7_0006'
logfile = 'conf/2003846667223680600001_r12_insertion_R_6_5_7_0006.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.8174775245024661), np.float64(0.5512973589989103), np.float64(1.1902244688562518)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.32583223608967876), np.float64(-1.2836671758062865), np.float64(-0.20473025911259934)], [np.float64(-0.3123019984282574), np.float64(0.7006250078006182), np.float64(-1.0989952274996915)], [np.float64(2.0418452207807034), np.float64(0.0), np.float64(0.0)], [np.float64(1.9521805275866726), np.float64(-0.5144889962524692), np.float64(1.4552813225457637)], [np.float64(3.534719139045433), np.float64(-0.2666039324647221), np.float64(0.5773745363975276)], [np.float64(2.0539661386427035), np.float64(1.621307463087795), np.float64(0.0)], [np.float64(-0.6437603260120839), np.float64(-0.20480683095863547), np.float64(2.2676884959858343)], [np.float64(-0.4485049061078451), np.float64(1.7970580632693127), np.float64(1.472464575706302)], [np.float64(-2.117080429644999), np.float64(0.5555626333789337), np.float64(0.8854388149393558)], [np.float64(1.9724113397530276), np.float64(1.93542529728666), np.float64(-0.9095585175140072)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r12_insertion_R_6_5_7_0006', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
