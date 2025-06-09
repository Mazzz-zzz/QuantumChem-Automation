import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003846467324380000001_0005'
logfile = 'conf/2003846467324380000001_0005.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(1.5579294246470219), np.float64(0.0), np.float64(0.0)], [np.float64(1.500408593933407), np.float64(0.022685859353132276), np.float64(2.603338958058368)], [np.float64(1.9532869110694588), np.float64(-0.7262151344707004), np.float64(-1.0748410376294886)], [np.float64(2.3263786123746657), np.float64(-0.804595943578375), np.float64(1.5076843761619838)], [np.float64(3.6913683576927516), np.float64(-0.4117410756232486), np.float64(1.6349478728388591)], [np.float64(1.8707995598600025), np.float64(-2.1524001806160418), np.float64(1.5750056260549825)], [np.float64(2.073726026013009), np.float64(1.2444094924446283), np.float64(0.0)], [np.float64(-0.5011159442462444), np.float64(-1.2223160330602842), np.float64(-0.0046407335589215256)], [np.float64(-0.4813959413250844), np.float64(0.6726726243990823), np.float64(1.0331118763487264)], [np.float64(-0.38920970649705977), np.float64(0.6300621149189147), np.float64(-1.122175824589612)], [np.float64(1.6529732059277755), np.float64(1.788883589623107), np.float64(-0.6751579342390955)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003846467324380000001_0005', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
