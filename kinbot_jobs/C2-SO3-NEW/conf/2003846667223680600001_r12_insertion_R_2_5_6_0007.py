import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003846667223680600001_r12_insertion_R_2_5_6_0007'
logfile = 'conf/2003846667223680600001_r12_insertion_R_2_5_6_0007.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.5887308291299226), np.float64(-1.3973946311450482), np.float64(-0.2907344552181208)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.5078246399554086), np.float64(0.9152262908701686), np.float64(-0.8082795140160011)], [np.float64(-0.37827293559623293), np.float64(0.4208768959605888), np.float64(1.2221470372131198)], [np.float64(1.9277442911557117), np.float64(0.0), np.float64(0.0)], [np.float64(1.3072199692205377), np.float64(0.8484084963490272), np.float64(2.4636180795648355)], [np.float64(2.3489727721135067), np.float64(-0.27030381822235994), np.float64(-1.363993049042664)], [np.float64(2.158020035648276), np.float64(1.5970768001692506), np.float64(0.0)], [np.float64(-0.5154829765357816), np.float64(-1.741841418837016), np.float64(-1.5656363326215483)], [np.float64(0.03071792342371095), np.float64(-2.366714553761543), np.float64(0.3821202823493221)], [np.float64(-1.8701634858288947), np.float64(-1.509021292957061), np.float64(0.04105333478053283)], [np.float64(1.808357830879297), np.float64(2.074435473323932), np.float64(-0.7846229512327535)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846667223680600001_r12_insertion_R_2_5_6_0007', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999'}
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
