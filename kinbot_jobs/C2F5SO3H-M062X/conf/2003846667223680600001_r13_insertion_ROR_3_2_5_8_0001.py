import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_8_0001'
logfile = 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_8_0001.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(1.8011152879658407), np.float64(-0.655222653097207), np.float64(-1.2772905174114781)], [np.float64(1.9720391950367426), np.float64(0.18089612227577465), np.float64(0.016354768994211285)], [np.float64(-0.566996631957985), np.float64(0.09966247117670347), np.float64(0.3670300988479033)], [np.float64(1.891152309196372), np.float64(-0.4476535591202117), np.float64(1.092670060720662)], [np.float64(2.1595605697114317), np.float64(2.003854547796319), np.float64(0.020457666298594863)], [np.float64(2.9349992064674804), np.float64(2.2096675530401124), np.float64(1.1897921912404545)], [np.float64(2.741404719007171), np.float64(2.247673633831246), np.float64(-1.251081524536528)], [np.float64(0.7089239756054887), np.float64(2.0871459988156227), np.float64(0.14226455119227008)], [np.float64(1.0115224731833432), np.float64(-0.08714256520502542), np.float64(-2.149449931915222)], [np.float64(2.981353074501861), np.float64(-0.8336702901796945), np.float64(-1.8661815630746095)], [np.float64(1.3249071168152513), np.float64(-1.858016147591797), np.float64(-1.0508040868119162)], [np.float64(-0.7576002955329947), np.float64(1.0124298882581586), np.float64(0.388332286455659)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_8_0001', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
