import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = '1642764945472630600001_R_Addition_MultipleBond_1_3_4_IRC_R'
logfile = '1642764945472630600001_R_Addition_MultipleBond_1_3_4_IRC_R.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')], positions=[[np.float64(1.730899), np.float64(0.113914), np.float64(-0.239177)], [np.float64(2.639855), np.float64(-0.679418), np.float64(0.079833)], [np.float64(0.291921), np.float64(-0.226299), np.float64(-0.187706)], [np.float64(-0.28884), np.float64(0.482988), np.float64(2.243421)], [np.float64(-1.099015), np.float64(1.383466), np.float64(1.557328)], [np.float64(-0.678457), np.float64(-0.851927), np.float64(2.309643)], [np.float64(1.073496), np.float64(0.777095), np.float64(2.367956)], [np.float64(-0.62824), np.float64(0.524592), np.float64(-0.869126)], [np.float64(-0.048026), np.float64(-1.55136), np.float64(-0.121219)], [np.float64(1.896688), np.float64(1.447803), np.float64(-0.570005)], [np.float64(2.846505), np.float64(1.702789), np.float64(-0.509822)]])

kwargs = {'method': 'mp2', 'basis': '6-31G', 'nprocshared': 8, 'mem': '28GB', 'chk': '1642764945472630600001_R_Addition_MultipleBond_1_3_4_IRC_R', 'label': '1642764945472630600001_R_Addition_MultipleBond_1_3_4_IRC_R', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'guess': 'Read,Mix', 'geom': 'AllCheck,NoKeepConstants', 'irc': 'RCFC,reverse,MaxPoints=100,StepSize=2'}
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
    label = '1642764945472630600001_R_Addition_MultipleBond_1_3_4_IRC_R_prod'
    logfile = '1642764945472630600001_R_Addition_MultipleBond_1_3_4_IRC_R_prod.log'
    # start the product optimization
    prod_kwargs = {'method': 'mp2', 'basis': '6-31G', 'nprocshared': 8, 'mem': '28GB', 'chk': '1642764945472630600001_R_Addition_MultipleBond_1_3_4_IRC_R_prod', 'label': '1642764945472630600001_R_Addition_MultipleBond_1_3_4_IRC_R_prod', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'guess': 'Mix,Always', 'freq': 'freq', 'opt': 'CalcFC'}
    calc_prod = Gaussian(**prod_kwargs)
    mol_prod = Atoms(symbols=[np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')], positions=mol.positions)
    mol_prod.calc = calc_prod
    try:
        e = mol_prod.get_potential_energy() # use the Gaussian optimizer
        iowait(logfile, 'gauss')
        mol_prod.positions = reader_gauss.read_geom(logfile, 
                                                    mol_prod, 
                                                    max2frag=True, 
                                                    charge=kwargs['charge'],
                                                    mult=kwargs['mult'])
        freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')])
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
                freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')])
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
