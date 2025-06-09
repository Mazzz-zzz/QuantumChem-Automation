import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = '2003846667223680600001_r12_insertion_R_9_1_10_IRC_F'
logfile = '2003846667223680600001_r12_insertion_R_9_1_10_IRC_F.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-1.061763), np.float64(-0.14689), np.float64(1.024145)], [np.float64(-0.426978), np.float64(0.640948), np.float64(0.06014)], [np.float64(-0.568073), np.float64(0.285147), np.float64(-1.200221)], [np.float64(-0.474803), np.float64(1.953604), np.float64(0.240388)], [np.float64(1.847095), np.float64(0.033097), np.float64(0.541032)], [np.float64(2.652575), np.float64(0.68619), np.float64(1.541196)], [np.float64(2.047132), np.float64(-1.201201), np.float64(-0.154817)], [np.float64(1.93613), np.float64(1.129863), np.float64(-0.699098)], [np.float64(-1.448539), np.float64(0.325), np.float64(2.143498)], [np.float64(0.765937), np.float64(-0.744654), np.float64(1.873622)], [np.float64(-1.424654), np.float64(-1.341343), np.float64(0.773447)], [np.float64(2.206364), np.float64(1.978271), np.float64(-0.325035)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'chk': '2003846667223680600001_r12_insertion_R_9_1_10_IRC_F', 'label': '2003846667223680600001_r12_insertion_R_9_1_10_IRC_F', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'geom': 'AllCheck,NoKeepConstants', 'guess': 'Read', 'irc': 'RCFC,forward,MaxPoints=100,StepSize=2'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

success = True

try:
    e = mol.get_potential_energy()  # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    db.write(mol, name=label, data={'energy': e, 'status': 'normal'})
except RuntimeError:
    # Retry by correcting errors
    try:
        iowait(logfile, 'gauss')
        mol.positions = reader_gauss.read_geom(logfile, mol)
        kwargs = reader_gauss.correct_kwargs(logfile, kwargs)
        mol.calc = Gaussian(**kwargs)
        e = mol.get_potential_energy()  # use the Gaussian optimizer
        iowait(logfile, 'gauss')
        mol.positions = reader_gauss.read_geom(logfile, mol)
        db.write(mol, name=label, data={'energy': e, 'status': 'normal'})
    except RuntimeError:
        if mol.positions is not None:
            # although there is an error, continue from the final geometry
            db.write(mol, name=label, data={'status': 'normal'})
        else:
            db.write(mol, name=label, data={'status': 'error'})
            success = False

with open(logfile, 'a') as f:
    f.write('done\n')

if success:
    label = '2003846667223680600001_r12_insertion_R_9_1_10_IRC_F_prod'
    logfile = '2003846667223680600001_r12_insertion_R_9_1_10_IRC_F_prod.log'
    # start the product optimization
    prod_kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'chk': '2003846667223680600001_r12_insertion_R_9_1_10_IRC_F_prod', 'label': '2003846667223680600001_r12_insertion_R_9_1_10_IRC_F_prod', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC'}
    calc_prod = Gaussian(**prod_kwargs)
    mol_prod = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=mol.positions)
    mol_prod.calc = calc_prod
    try:
        e = mol_prod.get_potential_energy() # use the Gaussian optimizer
        iowait(logfile, 'gauss')
        mol_prod.positions = reader_gauss.read_geom(logfile, 
                                                    mol_prod, 
                                                    max2frag=True, 
                                                    charge=kwargs['charge'],
                                                    mult=kwargs['mult'])
        freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')])
        zpe = reader_gauss.read_zpe(logfile)
        db.write(mol_prod, name=label, data={'energy': e,
                                         'frequencies': np.asarray(freq),
                                         'zpe': zpe, 'status': 'normal'})
    except RuntimeError: 
        for i in range(3):
            try:
                iowait(logfile, 'gauss')
                _, mol_prod.positions = reader_gauss.read_lowest_geom_energy(logfile, mol_prod)
                prod_kwargs = reader_gauss.correct_kwargs(logfile, prod_kwargs)
                mol_prod.calc = Gaussian(**prod_kwargs)
                e = mol_prod.get_potential_energy()  # use the Gaussian optimizer
                iowait(logfile, 'gauss')
                mol_prod.positions = reader_gauss.read_geom(logfile, mol_prod)
                freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')])
                zpe = reader_gauss.read_zpe(logfile)
                db.write(mol_prod, name=label, data={'energy': e,
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
