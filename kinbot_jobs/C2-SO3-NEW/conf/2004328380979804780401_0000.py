import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2004328380979804780401_0000'
logfile = 'conf/2004328380979804780401_0000.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(0.22567145850095965), np.float64(-0.2722432153311833), np.float64(1.5367968394869858)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.5790950850960964), np.float64(-0.9561171755491061), np.float64(-0.6692235251412968)], [np.float64(-0.5703497721685482), np.float64(1.1419591995224614), np.float64(-0.2781201679154242)], [np.float64(1.9768644117399654), np.float64(0.0), np.float64(0.0)], [np.float64(1.6048020563077972), np.float64(-0.26153390350580774), np.float64(1.6078998270766995)], [np.float64(3.36046940403941), np.float64(-0.2982008286365062), np.float64(-0.2972660156418051)], [np.float64(2.11525997638529), np.float64(1.659856716376598), np.float64(0.0)], [np.float64(1.470861781321251), np.float64(-1.5995924522076514), np.float64(-0.39154628504259104)], [np.float64(-0.29639418571670506), np.float64(0.6872745129154378), np.float64(2.293438281925236)], [np.float64(-0.27127439262563885), np.float64(-1.4371355725357793), np.float64(1.927199868475465)], [np.float64(1.7291961586611349), np.float64(2.0005535767577434), np.float64(-0.8154187575642842)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2004328380979804780401_0000', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
