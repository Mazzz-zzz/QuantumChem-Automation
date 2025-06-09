import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003716027184320770001_0013'
logfile = 'conf/2003716027184320770001_0013.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.658715803029013), np.float64(0.37211403115733865), np.float64(-1.3460146581838095)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.44954833216753126), np.float64(0.7559579784834439), np.float64(0.9694481730539365)], [np.float64(-0.469018357979435), np.float64(-1.326358916292835), np.float64(0.3185483677273704)], [np.float64(1.9504085506544522), np.float64(0.0), np.float64(0.0)], [np.float64(-1.8793879142389232), np.float64(-1.69772673925742), np.float64(-0.4113350946588934)], [np.float64(2.250186222116059), np.float64(-0.41945114985970544), np.float64(-1.360447206183109)], [np.float64(2.044140986139139), np.float64(1.6315803765466503), np.float64(0.0)], [np.float64(-0.3144764632200728), np.float64(1.6169133252308774), np.float64(-1.653761106551494)], [np.float64(-0.2343415798841926), np.float64(-0.4460119716682488), np.float64(-2.2994381526042362)], [np.float64(-1.9812987006929068), np.float64(0.2956844028556935), np.float64(-1.2607514616999154)], [np.float64(1.4065647916359207), np.float64(1.9538276124006848), np.float64(-0.666038801026059)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003716027184320770001_0013', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
