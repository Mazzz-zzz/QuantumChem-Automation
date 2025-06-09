import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = 'conf/2003686066703381580601_0025'
logfile = 'conf/2003686066703381580601_0025.log'

mol = Atoms(symbols=['C', 'C', 'F', 'F', 'S', 'O', 'O', 'O', 'F', 'F', 'F', 'H'], positions=[[np.float64(-0.656359770778357), np.float64(4.97532558058025), np.float64(0.07329794727349576)], [np.float64(0.39345450777927415), np.float64(3.863576707848634), np.float64(0.3348898412448103)], [np.float64(1.541820427055138), np.float64(4.19967432666974), np.float64(-0.24646739797947292)], [np.float64(0.5669529220216762), np.float64(3.7415922841458267), np.float64(1.6554386696106012)], [np.float64(-0.2343027971532754), np.float64(2.171373660248706), np.float64(-0.3077895720806347)], [np.float64(0.9656734254322219), np.float64(0.0), np.float64(0.0)], [np.float64(-0.4069769465088614), np.float64(2.3732456796206494), np.float64(-1.7443263262655102)], [np.float64(1.2422391942639184), np.float64(1.3943354573833844), np.float64(0.0)], [np.float64(-0.7358882234679528), np.float64(5.25942234167806), np.float64(-1.2163868248764789)], [np.float64(-1.8521625969845767), np.float64(4.558667792653166), np.float64(0.5010552297806745)], [np.float64(-0.3256862446621383), np.float64(6.0761219199854635), np.float64(0.7387806105976038)], [np.float64(0.0), np.float64(0.0), np.float64(0.0)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'label': 'conf/2003686066703381580601_0025', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC, Tight'}
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
