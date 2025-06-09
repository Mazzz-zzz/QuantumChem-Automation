import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003846667223680600001_r13_insertion_ROR_12_8_5_6_0001'
logfile = 'conf/2003846667223680600001_r13_insertion_ROR_12_8_5_6_0001.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(3.97667136840345), np.float64(2.1222011134713883), np.float64(1.7837119024168993)], [np.float64(3.231530087682697), np.float64(0.8429504699546986), np.float64(1.3016429998295005)], [np.float64(4.0908874046414105), np.float64(-0.04588742759762078), np.float64(0.82936342590167)], [np.float64(2.6341172196169147), np.float64(0.23797893240634818), np.float64(2.3116933211710435)], [np.float64(1.9762821264492332), np.float64(1.2068485371033233), np.float64(-0.12224971556977816)], [np.float64(-0.31191553310274467), np.float64(1.0832876459381546), np.float64(0.16911370641551052)], [np.float64(2.4373556137689727), np.float64(2.3743080556737257), np.float64(-0.8576801464230268)], [np.float64(1.2267318990066431), np.float64(-0.004279867696457911), np.float64(-0.5685597301564294)], [np.float64(4.666660929800281), np.float64(2.714917227408121), np.float64(0.8258699866444164)], [np.float64(3.144117334319587), np.float64(3.0350700936211408), np.float64(2.274933762387354)], [np.float64(4.845807535622817), np.float64(1.861124860038325), np.float64(2.7531424749766895)], [np.float64(-0.6713479862092541), np.float64(1.1722423596788536), np.float64(1.0675750124061503)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r13_insertion_ROR_12_8_5_6_0001', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
