import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003846667223680600001_r12_insertion_R_2_5_6_0000'
logfile = 'conf/2003846667223680600001_r12_insertion_R_2_5_6_0000.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.6046351685277238), np.float64(-1.3826178959756452), np.float64(-0.3265368807230357)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.49225161761712255), np.float64(0.933470891670029), np.float64(-0.7969700373082336)], [np.float64(-0.2676588390547444), np.float64(0.31492549797793684), np.float64(1.2818158340113508)], [np.float64(1.9277442910692277), np.float64(0.0), np.float64(0.0)], [np.float64(1.4063423292926975), np.float64(0.9385469401449055), np.float64(2.453880821751787)], [np.float64(2.388081277581995), np.float64(-0.4952349668597931), np.float64(-1.2860042034658066)], [np.float64(2.063094770960044), np.float64(1.6079059274855994), np.float64(0.0)], [np.float64(-0.4651962501762099), np.float64(-1.645869669675028), np.float64(-1.6151946799521752)], [np.float64(0.02893694691481081), np.float64(-2.314250203893736), np.float64(0.3852769869016994)], [np.float64(-1.8958148873167933), np.float64(-1.4082642236859342), np.float64(-0.015393023493368102)], [np.float64(2.93871807039345), np.float64(1.7749233513923932), np.float64(-0.4137114372299782)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r12_insertion_R_2_5_6_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
