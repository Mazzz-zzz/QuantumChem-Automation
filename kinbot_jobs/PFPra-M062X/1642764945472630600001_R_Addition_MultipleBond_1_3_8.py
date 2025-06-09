import numpy as np
from ase import Atoms
from ase.db import connect

from kinbot.ase_modules.calculators.gaussian import Gaussian
from kinbot import reader_gauss
from kinbot.utils import iowait

db = connect('/home/akhalilov/GaussianJobCreator/AUTOMATION-CENTER/kinbot_jobs/PFPra-M062X/kinbot.db')
label = '1642764945472630600001_R_Addition_MultipleBond_1_3_8'
logfile = '1642764945472630600001_R_Addition_MultipleBond_1_3_8.log'

atom = [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')]
geom = [[np.float64(1.5999404896015312), np.float64(-0.04446294241671958), np.float64(-0.101365695234793)], [np.float64(2.205680297606539), np.float64(-0.8375190439698591), np.float64(-0.7479084300218399)], [np.float64(0.08056071756111298), np.float64(-0.1313847370057511), np.float64(0.1253382899600131)], [np.float64(-0.6022885465333132), np.float64(0.4678145949908446), np.float64(1.3634152231035161)], [np.float64(-1.9033261308873184), np.float64(0.22854694649864232), np.float64(1.3248263900208515)], [np.float64(-0.09341393202746653), np.float64(-0.11278218764344194), np.float64(2.443689192018598)], [np.float64(-0.41375155140414177), np.float64(1.7772530157316468), np.float64(1.4368682526663146)], [np.float64(-0.1327596979270657), np.float64(0.7310524938995859), np.float64(-0.9748494292840625)], [np.float64(-0.4401707088963325), np.float64(-1.3165521417635746), np.float64(-0.16063182898148648)], [np.float64(2.0775766690875077), np.float64(1.0559212586529871), np.float64(0.4698345661934594)], [np.float64(3.013216513250005), np.float64(1.2108207629820318), np.float64(0.27282064609348067)]]
mol = Atoms(symbols=atom, positions=geom)

kwargs = {'method': 'mp2', 'basis': '6-31G', 'nprocshared': 8, 'mem': '28GB', 'chk': '1642764945472630600001_R_Addition_MultipleBond_1_3_8', 'label': '1642764945472630600001_R_Addition_MultipleBond_1_3_8', 'Symm': 'None', 'mult': 1, 'charge': 0, 'scf': 'xqc', 'pop': 'None', 'guess': 'Mix,Always', 'opt': 'NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999', 'addsec': '1 2 F\n1 3 F\n1 10 F\n3 4 F\n3 8 F\n3 9 F\n4 5 F\n4 6 F\n4 7 F\n10 11 F\n1 3 8 F\n'}
Gaussian.command = 'g16 < PREFIX.com > PREFIX.log'
calc = Gaussian(**kwargs)
mol.calc = calc

try:
    e = mol.get_potential_energy() # use the Gaussian optimizer
    iowait(logfile, 'gauss')
    mol.positions = reader_gauss.read_geom(logfile, mol)
    freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')])
    zpe = reader_gauss.read_zpe(logfile)
    db.write(mol, name=label, data={'energy': e,'frequencies': np.asarray(freq), 'zpe':zpe, 'status': 'normal'})
except RuntimeError:
    try:
        iowait(logfile, 'gauss')
        mol.positions = reader_gauss.read_geom(logfile, mol)
        kwargs = reader_gauss.correct_kwargs(logfile, kwargs)
        mol.calc = Gaussian(**kwargs)
        e = mol.get_potential_energy()  # use the Gaussian optimizer
        iowait(logfile, 'gauss')
        mol.positions = reader_gauss.read_geom(logfile, mol)
        freq = reader_gauss.read_freq(logfile, [np.str_('C'), np.str_('O'), np.str_('C'), np.str_('C'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('F'), np.str_('O'), np.str_('H')])
        zpe = reader_gauss.read_zpe(logfile)
        db.write(mol, name=label, data={'energy': e,
                                         'frequencies': np.asarray(freq),
                                         'zpe': zpe, 'status': 'normal'})
    except RuntimeError:
        db.write(mol, name=label, data={'status': 'error'})

with open(logfile,'a') as f:
    f.write('done\n')
