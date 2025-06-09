import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003716027184320770001_0010'
logfile = 'conf/2003716027184320770001_0010.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.658715803029013), np.float64(0.9796258722747375), np.float64(0.9952675331787941)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)], [np.float64(-0.44954833216753143), np.float64(-1.217545734758844), np.float64(0.16995472703322403)], [np.float64(-0.46901835797943503), np.float64(0.38730847936044754), np.float64(-1.3079346999092785)], [np.float64(1.9504085506544522), np.float64(0.0), np.float64(0.0)], [np.float64(-1.8793879142389223), np.float64(1.205090011071389), np.float64(-1.2646069375515996)], [np.float64(2.2501862221160596), np.float64(-0.4194511498597058), np.float64(-1.3604472061831088)], [np.float64(2.044140986139139), np.float64(1.6315803765466506), np.float64(0.0)], [np.float64(-0.3144764632200728), np.float64(0.6237424674488184), np.float64(2.2271685686432567)], [np.float64(-0.2343415798841926), np.float64(2.2143778404205516), np.float64(0.7634613784454287)], [np.float64(-1.9812987006929068), np.float64(0.9440005922626439), np.float64(0.8864459352258204)], [np.float64(1.4065647916359212), np.float64(1.9538276124006857), np.float64(-0.6660388010260588)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003716027184320770001_0010', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
