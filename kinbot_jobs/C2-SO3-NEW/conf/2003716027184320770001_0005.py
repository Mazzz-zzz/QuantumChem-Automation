import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003716027184320770001_0005'
logfile = 'conf/2003716027184320770001_0005.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.6587158030290123), np.float64(0.3721140311573388), np.float64(-1.34601465818381)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.4495483321675315), np.float64(0.7559579784834433), np.float64(0.9694481730539375)], [np.float64(-0.46901835797943503), np.float64(-1.3263589162928353), np.float64(0.31854836772737044)], [np.float64(1.9504085506544517), np.float64(0.0), np.float64(0.0)], [np.float64(-0.7276799896298881), np.float64(-1.5465982473162276), np.float64(1.9136580853343736)], [np.float64(2.250186222116061), np.float64(-0.4194511498597048), np.float64(-1.3604472061831079)], [np.float64(2.044140986139139), np.float64(1.6315803765466503), np.float64(0.0)], [np.float64(-0.3144764632200723), np.float64(1.6169133252308774), np.float64(-1.653761106551494)], [np.float64(-0.23434157988419207), np.float64(-0.4460119716682493), np.float64(-2.2994381526042362)], [np.float64(-1.9812987006929068), np.float64(0.29568440285569286), np.float64(-1.2607514616999156)], [np.float64(1.8116038338461922), np.float64(1.9305585804617804), np.float64(0.9002737781764882)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003716027184320770001_0005', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
