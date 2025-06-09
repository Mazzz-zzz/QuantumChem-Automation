import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_0003'
logfile = 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_0003.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(1.8559861217159654), np.float64(-0.8022795178353822), np.float64(-1.1154124953579865)], [np.float64(1.9102844727625665), np.float64(0.009201630897838521), np.float64(0.14815600813393426)], [np.float64(-0.5573142058203007), np.float64(1.067486088832173), np.float64(-0.689571997864426)], [np.float64(2.1516280316936847), np.float64(-0.7049957502562312), np.float64(1.244906200445844)], [np.float64(1.8221219194604807), np.float64(1.6667517980344289), np.float64(0.27426293701799914)], [np.float64(0.3165050804680028), np.float64(1.9028013409479623), np.float64(0.5278690700072269)], [np.float64(2.621856743261549), np.float64(2.4108801709279843), np.float64(1.1882286564501694)], [np.float64(1.9323335971732802), np.float64(2.296377221136845), np.float64(-1.1586306439842784)], [np.float64(1.6366187561744159), np.float64(-0.05999443143694903), np.float64(-2.207388469728494)], [np.float64(2.9841557411921174), np.float64(-1.472182992435539), np.float64(-1.3795770437410542)], [np.float64(0.8945019911733344), np.float64(-1.724213897016348), np.float64(-1.1353444712673046)], [np.float64(1.3580717507449007), np.float64(2.042888338203219), np.float64(-1.8998597501116306)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_0003', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
