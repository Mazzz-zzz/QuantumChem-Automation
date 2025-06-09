import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1642764945472630600001_r13_insertion_ROR_4_3_1_2_0003'
logfile = 'conf/1642764945472630600001_r13_insertion_ROR_4_3_1_2_0003.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')], positions=[[np.float64(2.1599532381231232), np.float64(1.095660262379118), np.float64(-0.11389317433311463)], [np.float64(1.1004499472445544), np.float64(1.7157797808270163), np.float64(-0.348555783491455)], [np.float64(1.983741378114704), np.float64(-0.3371785463115221), np.float64(-0.17069882821388513)], [np.float64(-0.2259877587416057), np.float64(0.46896710570913147), np.float64(0.0405535352335739)], [np.float64(-0.5533103557311092), np.float64(-0.7702317319741341), np.float64(0.3021082989259941)], [np.float64(-0.47072379283133303), np.float64(1.2068937500818933), np.float64(1.1035700694946424)], [np.float64(-0.8154801373194589), np.float64(0.8590258299934771), np.float64(-1.0513504100604996)], [np.float64(2.3334322151656064), np.float64(-0.9859764758387093), np.float64(-1.292218076571409)], [np.float64(2.3715426020275845), np.float64(-1.116277337129137), np.float64(0.8673549258230957)], [np.float64(3.2840011178066884), np.float64(1.7378470264948929), np.float64(0.05481056884582915)], [np.float64(3.160807546141245), np.float64(2.6959303357679723), np.float64(-0.005706125652771953)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1642764945472630600001_r13_insertion_ROR_4_3_1_2_0003', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')])
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
            freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')])
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
