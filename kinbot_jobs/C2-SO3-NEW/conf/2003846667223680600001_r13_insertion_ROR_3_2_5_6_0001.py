import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_0001'
logfile = 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_0001.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(1.8566451194978117), np.float64(-0.7857513912277538), np.float64(-1.2085605969148614)], [np.float64(1.8695935808105617), np.float64(0.025923161051949754), np.float64(0.05598362413029843)], [np.float64(-0.6914760512076334), np.float64(0.8679463014834707), np.float64(0.8576798350061342)], [np.float64(2.075063144774915), np.float64(-0.6729664805141365), np.float64(1.169770463949673)], [np.float64(1.706851643032745), np.float64(1.6808585078462663), np.float64(0.1324833596718875)], [np.float64(0.20959561208101035), np.float64(1.8867546568382028), np.float64(-0.18806098422658352)], [np.float64(2.1210524581993324), np.float64(2.461039630215753), np.float64(1.2497976668035042)], [np.float64(2.2276702043210284), np.float64(2.349761239639757), np.float64(-1.1877726622373623)], [np.float64(1.7385142819703436), np.float64(-0.0320617137590823), np.float64(-2.3083413454560566)], [np.float64(2.9635810809279555), np.float64(-1.5090495952024798), np.float64(-1.4155696569284868)], [np.float64(0.8555065666582291), np.float64(-1.6610728597279567), np.float64(-1.2882220235288708)], [np.float64(1.9941523589336982), np.float64(2.0213385433560105), np.float64(-2.0715496802692748)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_0001', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
