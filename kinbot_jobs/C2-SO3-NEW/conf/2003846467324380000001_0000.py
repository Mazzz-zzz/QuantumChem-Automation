import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003846467324380000001_0000'
logfile = 'conf/2003846467324380000001_0000.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(1.5579294246470219), np.float64(0.0), np.float64(0.0)], [np.float64(3.838697169056535), np.float64(-0.3743862142095966), np.float64(1.1996376467066825)], [np.float64(1.9532869110694593), np.float64(-0.7262151344707007), np.float64(-1.0748410376294883)], [np.float64(2.326378612374666), np.float64(-0.8045959435783746), np.float64(1.5076843761619834)], [np.float64(2.268546862057722), np.float64(-2.2248522802061386), np.float64(1.392552379697222)], [np.float64(1.9144269557605946), np.float64(-0.07664304579328024), np.float64(2.660524823220122)], [np.float64(2.0737260260130084), np.float64(1.2444094924446283), np.float64(0.0)], [np.float64(-0.5011159442462444), np.float64(-1.2223160330602842), np.float64(-0.0046407335589215256)], [np.float64(-0.4813959413250844), np.float64(0.6726726243990823), np.float64(1.0331118763487264)], [np.float64(-0.38920970649705977), np.float64(0.6300621149189142), np.float64(-1.1221758245896123)], [np.float64(1.9403147365835856), np.float64(1.6697830959002482), np.float64(0.8547408610859548)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846467324380000001_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
