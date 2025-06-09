import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003846467324380000001_0006'
logfile = 'conf/2003846467324380000001_0006.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(1.5579294246470219), np.float64(0.0), np.float64(0.0)], [np.float64(1.8708653106814332), np.float64(-2.30378087334348), np.float64(1.172971373722993)], [np.float64(1.9532869110694593), np.float64(-0.7262151344707001), np.float64(-1.0748410376294883)], [np.float64(2.3263786123746666), np.float64(-0.8045959435783747), np.float64(1.5076843761619834)], [np.float64(1.6263909634687594), np.float64(-0.41292524973277966), np.float64(2.686810878555891)], [np.float64(3.7427326908509384), np.float64(-0.7593838436798448), np.float64(1.3643048952018482)], [np.float64(2.0737260260130084), np.float64(1.2444094924446285), np.float64(0.0)], [np.float64(-0.5011159442462444), np.float64(-1.2223160330602842), np.float64(-0.0046407335589215256)], [np.float64(-0.4813959413250844), np.float64(0.6726726243990823), np.float64(1.0331118763487264)], [np.float64(-0.38920970649705977), np.float64(0.6300621149189142), np.float64(-1.1221758245896123)], [np.float64(1.9403147365835856), np.float64(1.6697830959002478), np.float64(0.8547408610859542)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846467324380000001_0006', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, ['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'])
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
            freq = reader_gauss.read_freq(logfile, ['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'])
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
