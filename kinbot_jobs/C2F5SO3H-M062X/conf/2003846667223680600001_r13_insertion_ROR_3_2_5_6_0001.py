import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_0001'
logfile = 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_0001.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(1.7866199824073707), np.float64(-0.9727523754054161), np.float64(-1.1309514342757276)], [np.float64(2.2432902080983275), np.float64(0.032553928312270865), np.float64(-0.10069012251486742)], [np.float64(-0.28859369963187254), np.float64(0.3472539691658818), np.float64(0.10307449815652232)], [np.float64(3.005455181618754), np.float64(-0.4766163136802045), np.float64(0.846199923810602)], [np.float64(1.892064126695543), np.float64(1.6705155846959303), np.float64(-0.046672726385273984)], [np.float64(0.4254642842613222), np.float64(1.8965219710154815), np.float64(-0.18223167297108503)], [np.float64(2.473695268565662), np.float64(2.413312729118035), np.float64(1.0046744107897434)], [np.float64(2.358605895158024), np.float64(2.2746887977044263), np.float64(-1.3983664169785226)], [np.float64(1.0165166398444094), np.float64(-0.455623230372847), np.float64(-2.0746114779659)], [np.float64(2.808847311191262), np.float64(-1.5372687019682496), np.float64(-1.7907081227948711)], [np.float64(1.0993852035757243), np.float64(-1.9880688211363036), np.float64(-0.6306106445007055)], [np.float64(3.188731598215474), np.float64(2.064709462550996), np.float64(-1.853125214369914)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_ROR_3_2_5_6_0001', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
