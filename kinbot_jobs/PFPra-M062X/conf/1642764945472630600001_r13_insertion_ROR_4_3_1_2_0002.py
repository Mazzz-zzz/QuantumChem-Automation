import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1642764945472630600001_r13_insertion_ROR_4_3_1_2_0002'
logfile = 'conf/1642764945472630600001_r13_insertion_ROR_4_3_1_2_0002.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')], positions=[[np.float64(2.172136122771551), np.float64(1.105160460452984), np.float64(-0.10641188396509638)], [np.float64(1.1033462110130137), np.float64(1.7492168432775985), np.float64(-0.03540849885387342)], [np.float64(1.981778360394508), np.float64(-0.32699074549815793), np.float64(-0.10978814909896498)], [np.float64(-0.2396795732054039), np.float64(0.4619291210024107), np.float64(0.03209674652055805)], [np.float64(-0.580798310526629), np.float64(-0.8001275983480682), np.float64(0.07699169793315169)], [np.float64(-0.6068261795313109), np.float64(1.0419495342902296), np.float64(1.1560252522790426)], [np.float64(-0.7098105869694833), np.float64(1.0049897908516172), np.float64(-1.052321633486391)], [np.float64(2.286057722357056), np.float64(-1.037418400932607), np.float64(-1.2069364883102875)], [np.float64(2.4066009165769096), np.float64(-1.0515005129533388), np.float64(0.9530155546616842)], [np.float64(3.315980329415698), np.float64(1.7312701379102484), np.float64(-0.16930483894322407)], [np.float64(3.19964098770409), np.float64(2.6919613699470837), np.float64(-0.15198275873659944)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1642764945472630600001_r13_insertion_ROR_4_3_1_2_0002', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
