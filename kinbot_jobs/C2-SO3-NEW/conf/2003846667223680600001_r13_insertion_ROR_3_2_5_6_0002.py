import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_0002'
logfile = 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_0002.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(1.8718549894837229), np.float64(-0.792639945884917), np.float64(-1.1588408680772102)], [np.float64(1.8780998151074277), np.float64(0.013160856262483707), np.float64(0.10950506175104949)], [np.float64(-0.8344149240536529), np.float64(0.7553165484615522), np.float64(0.06190084459055388)], [np.float64(2.0197181479362363), np.float64(-0.7019886746026512), np.float64(1.2229191771517016)], [np.float64(1.8005989557758766), np.float64(1.6733775216712616), np.float64(0.20343264249304485)], [np.float64(0.29953004989949666), np.float64(2.037886763197928), np.float64(0.17440377218691122)], [np.float64(2.4796243565175637), np.float64(2.413051216959214), np.float64(1.2136026724162818)], [np.float64(2.187066691775625), np.float64(2.276037949053083), np.float64(-1.1927055670046343)], [np.float64(1.6766289974861055), np.float64(-0.044825972749126704), np.float64(-2.2516271202253892)], [np.float64(3.0074195457644186), np.float64(-1.4590603065346102), np.float64(-1.3990435026936685)], [np.float64(0.913671430336518), np.float64(-1.7170393979503176), np.float64(-1.2055520706018785)], [np.float64(1.6269519439706621), np.float64(2.1794434421161015), np.float64(-1.9803570419867613)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_0002', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
