import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = 'conf/1642764945472630600001_r13_insertion_ROR_4_3_1_2_0001'
logfile = 'conf/1642764945472630600001_r13_insertion_ROR_4_3_1_2_0001.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')], positions=[[np.float64(2.1628443698479214), np.float64(1.0927360135675752), np.float64(-0.09778458122361482)], [np.float64(1.1414292414818503), np.float64(1.7111693009229016), np.float64(0.27158783050054963)], [np.float64(1.9875901149037183), np.float64(-0.34042841873266366), np.float64(-0.04621552372121611)], [np.float64(-0.22773957241740228), np.float64(0.4753013082590687), np.float64(0.01979556829922198)], [np.float64(-0.593060667953099), np.float64(-0.7685969864192781), np.float64(-0.1555847713767689)], [np.float64(-0.7065218483844411), np.float64(0.9031381947261705), np.float64(1.169898823179667)], [np.float64(-0.5667586475582524), np.float64(1.181837382185341), np.float64(-1.0185924098118442)], [np.float64(2.255619931628336), np.float64(-1.1081100107229953), np.float64(-1.11389391047132)], [np.float64(2.4601885740105347), np.float64(-1.0028856457284772), np.float64(1.0367459010827083)], [np.float64(3.262458687218396), np.float64(1.734574991798688), np.float64(-0.3863053499298506)], [np.float64(3.152375817222435), np.float64(2.6917038701436686), np.float64(-0.293676576527532)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/1642764945472630600001_r13_insertion_ROR_4_3_1_2_0001', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
