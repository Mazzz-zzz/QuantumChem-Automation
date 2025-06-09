import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/C2F5SO3H-M062X/kinbot.db')
label = '2003846667223680600001_R_Addition_MultipleBond_5_8_12_IRC_F'
logfile = '2003846667223680600001_R_Addition_MultipleBond_5_8_12_IRC_F.log'

mol = Atoms(symbols=[np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('S'), np.str_('O'), np.str_('O'), np.str_('O'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('H')], positions=[[np.float64(-0.720703), np.float64(-1.362324), np.float64(0.302836)], [np.float64(-0.11738), np.float64(0.042758), np.float64(0.147009)], [np.float64(-0.394623), np.float64(0.562304), np.float64(-1.106057)], [np.float64(-0.550805), np.float64(0.894165), np.float64(1.15357)], [np.float64(1.882342), np.float64(0.045095), np.float64(0.268665)], [np.float64(2.355782), np.float64(-0.77925), np.float64(1.537656)], [np.float64(2.528015), np.float64(-0.241668), np.float64(-1.299783)], [np.float64(2.329826), np.float64(1.684488), np.float64(0.004566)], [np.float64(-0.015067), np.float64(-2.244057), np.float64(-0.514147)], [np.float64(-0.619696), np.float64(-1.781117), np.float64(1.61988)], [np.float64(-2.056007), np.float64(-1.350849), np.float64(-0.079836)], [np.float64(2.759124), np.float64(1.075687), np.float64(-1.125306)]])

kwargs = {'method': 'mp2', 'basis': '6-31G', 'nprocshared': 8, 'mem': '28GB', 'chk': '2003846667223680600001_R_Addition_MultipleBond_5_8_12_IRC_F', 'label': '2003846667223680600001_R_Addition_MultipleBond_5_8_12_IRC_F', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'guess': 'Read,Mix', 'geom': 'AllCheck,NoKeepConstants', 'irc': 'RCFC,forward,MaxPoints=100,StepSize=2'}
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
    label = '2003846667223680600001_R_Addition_MultipleBond_5_8_12_IRC_F_prod'
    logfile = '2003846667223680600001_R_Addition_MultipleBond_5_8_12_IRC_F_prod.log'
    # start the product optimization
    prod_kwargs = {'method': 'mp2', 'basis': '6-31G', 'nprocshared': 8, 'mem': '28GB', 'chk': '2003846667223680600001_R_Addition_MultipleBond_5_8_12_IRC_F_prod', 'label': '2003846667223680600001_R_Addition_MultipleBond_5_8_12_IRC_F_prod', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'guess': 'Mix,Always', 'freq': 'freq', 'opt': 'CalcFC'}
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
