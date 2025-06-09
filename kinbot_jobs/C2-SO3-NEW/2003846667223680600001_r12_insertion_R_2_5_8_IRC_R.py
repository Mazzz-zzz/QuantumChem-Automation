import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW/kinbot.db')
label = '2003846667223680600001_r12_insertion_R_2_5_8_IRC_R'
logfile = '2003846667223680600001_r12_insertion_R_2_5_8_IRC_R.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.893937), np.float64(-0.276039), np.float64(1.230376)], [np.float64(-0.010975), np.float64(0.598588), np.float64(0.255214)], [np.float64(-0.255378), np.float64(0.248677), np.float64(-1.012642)], [np.float64(-0.304889), np.float64(1.885263), np.float64(0.411218)], [np.float64(1.832149), np.float64(0.389775), np.float64(0.526956)], [np.float64(2.159892), np.float64(0.987383), np.float64(1.781368)], [np.float64(2.170889), np.float64(-0.955436), np.float64(0.15487)], [np.float64(2.345119), np.float64(1.391156), np.float64(-0.616263)], [np.float64(-0.12478), np.float64(-0.996114), np.float64(2.040349)], [np.float64(-1.665874), np.float64(0.509431), np.float64(1.965708)], [np.float64(-1.660691), np.float64(-1.099187), np.float64(0.530139)], [np.float64(2.458897), np.float64(0.914536), np.float64(-1.449009)]])

kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'chk': '2003846667223680600001_r12_insertion_R_2_5_8_IRC_R', 'label': '2003846667223680600001_r12_insertion_R_2_5_8_IRC_R', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'geom': 'AllCheck,NoKeepConstants', 'guess': 'Read', 'irc': 'RCFC,reverse,MaxPoints=100,StepSize=2'}
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
    label = '2003846667223680600001_r12_insertion_R_2_5_8_IRC_R_prod'
    logfile = '2003846667223680600001_r12_insertion_R_2_5_8_IRC_R_prod.log'
    # start the product optimization
    prod_kwargs = {'method': 'wb97xd', 'basis': '6-311++G(d,p)', 'nprocshared': 8, 'mem': '28GB', 'chk': '2003846667223680600001_r12_insertion_R_2_5_8_IRC_R_prod', 'label': '2003846667223680600001_r12_insertion_R_2_5_8_IRC_R_prod', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC'}
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
