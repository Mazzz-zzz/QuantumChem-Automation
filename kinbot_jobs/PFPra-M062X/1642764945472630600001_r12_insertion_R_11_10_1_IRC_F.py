import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = '1642764945472630600001_r12_insertion_R_11_10_1_IRC_F'
logfile = '1642764945472630600001_r12_insertion_R_11_10_1_IRC_F.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')], positions=[[np.float64(1.488439), np.float64(0.321464), np.float64(-0.028643)], [np.float64(2.319072), np.float64(-0.508558), np.float64(0.414426)], [np.float64(-0.019831), np.float64(0.089848), np.float64(-0.006988)], [np.float64(-0.605255), np.float64(0.295703), np.float64(1.409416)], [np.float64(-1.921222), np.float64(0.181591), np.float64(1.365117)], [np.float64(-0.117438), np.float64(-0.607023), np.float64(2.244012)], [np.float64(-0.285949), np.float64(1.50779), np.float64(1.846546)], [np.float64(-0.62129), np.float64(0.945999), np.float64(-0.834433)], [np.float64(-0.285145), np.float64(-1.161632), np.float64(-0.395477)], [np.float64(2.030648), np.float64(1.361538), np.float64(-0.471018)], [np.float64(2.947467), np.float64(0.544686), np.float64(-0.030854)]])

kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'chk': '1642764945472630600001_r12_insertion_R_11_10_1_IRC_F', 'label': '1642764945472630600001_r12_insertion_R_11_10_1_IRC_F', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'geom': 'AllCheck,NoKeepConstants', 'guess': 'Read', 'irc': 'RCFC,forward,MaxPoints=100,StepSize=2'}
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
    label = '1642764945472630600001_r12_insertion_R_11_10_1_IRC_F_prod'
    logfile = '1642764945472630600001_r12_insertion_R_11_10_1_IRC_F_prod.log'
    # start the product optimization
    prod_kwargs = {'method': 'M062X', 'basis': 'Def2TZVPP', 'nprocshared': 8, 'mem': '28GB', 'chk': '1642764945472630600001_r12_insertion_R_11_10_1_IRC_F_prod', 'label': '1642764945472630600001_r12_insertion_R_11_10_1_IRC_F_prod', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'freq': 'freq', 'opt': 'CalcFC'}
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
