import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1642764945472630600001_ketoenol_2_1_3_8_0002'
logfile = 'conf/1642764945472630600001_ketoenol_2_1_3_8_0002.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')], positions=[[np.float64(1.0344906185962952), np.float64(0.19296056554393512), np.float64(0.21053161600795586)], [np.float64(0.8723355444313348), np.float64(-0.839565114198269), np.float64(-0.4404527381333079)], [np.float64(1.555041620442529), np.float64(1.4178071038561595), np.float64(-0.23789045565111808)], [np.float64(1.0910453801847462), np.float64(2.1154969369429746), np.float64(-1.5163759873855174)], [np.float64(0.9756196813204804), np.float64(3.4346803174294047), np.float64(-1.3216209379073054)], [np.float64(1.9345869988984479), np.float64(1.9899549370596201), np.float64(-2.526125407178935)], [np.float64(-0.07906828828021231), np.float64(1.7175050052807075), np.float64(-1.9401503098496256)], [np.float64(1.5062633560273424), np.float64(-0.3120040558393152), np.float64(-2.1574775088142752)], [np.float64(2.386658445036443), np.float64(2.0699538035521003), np.float64(0.49174818536567877)], [np.float64(1.0806940631571162), np.float64(0.03804640786668794), np.float64(1.5364679291579626)], [np.float64(0.9596285801854797), np.float64(-0.8873499074940066), np.float64(1.7850186143884872)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1642764945472630600001_ketoenol_2_1_3_8_0002', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
