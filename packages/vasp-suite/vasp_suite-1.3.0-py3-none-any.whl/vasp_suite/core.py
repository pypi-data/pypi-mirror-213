'''
A programme which holds the core functions of vasp_suite.
'''

# Imports 
import numpy as np 
import os
from . import structure 
from . import input 
from . import submission
from . import ewald
import socket
# Functions 

def generate_input(filename: str, calculation: str) -> None:
    '''
    Generates Input files for VASP Calculations.
    '''
    input_files = input.InputFileGenerator(filename, calculation)
    input_files._INCAR()
    input_files._POTCAR()
    return None

def generate_job(title, cores, vasp_type):
    '''
    Generates a submission script for VASP calculations.
    '''
    job = submission.SubmissionWriter(title, cores, vasp_type)
    if job.hostname == 'csf3':
        job.submission_csf3() 
    elif job.hostname == 'csf4':
        job.submission_csf4() 
    else: 
        exit()

def generate_supercell(expansion: np.ndarray) -> None: 
    '''
    Generates a supercell from a given expansion matrix.
    '''
    _s = structure.Structure('POSCAR')
    _s.Vasp_reader()
    _s.Supercell(expansion)
    _s.supercell_reorder()
    _s.write_poscar()
    return None

def dope_structure(filename: str, dopant: str, replace: str, instances: int) -> None:
    '''
    Dopes a structure with a given dopant and generates all possible structures.
    '''
    _d = structure.DOPE(filename, dopant, replace, instances)
    _d.Generate_structure()
    _d.write_poscars()
    return None

def generate_defect(filename: str, site: str, instances: int) -> None:
    '''
    Generates a defect structure from a given structure.
    '''
    _d = structure.DOPE(filename, 'D', site, instances)
    _d.Generate_structure()
    _d.Create_defect()
    _d.write_poscars()
    return None

def asymmetric_unit(filename: str, atom: str, bond_max: float) -> None:
    '''
    Generates the asymmetric unit of a structure.
    '''
    _a = structure.Asymmetric_unit(filename, atom, bond_max)
    _a.find_unit()


def calculate_kpoints(filename: str) -> None:
    '''
    Calculates possible kpoint meshes for a given structure.
    '''
    _s = structure.Structure(filename) 
    _s.Vasp_reader() 
    mesh, density = _s.Calculate_mesh()
    for i in range(len(mesh)):
        print(f'Mesh: {mesh[i][0]} {mesh[i][1]} {mesh[i][2]} Density: {density[i]}')
    return None

def generate_kpoints(mesh: list) -> None:
    with open('KPOINTS', 'w') as f:
        f.write(f'''Regular {mesh[0]} {mesh[1]} {mesh[2]} gamma centred mesh \n''')
        f.write('0\nGamma\n')
        f.write(f'{mesh[0]} {mesh[1]} {mesh[2]}\n')
        f.write('0 0 0')

def convert_cif(filename: str) -> None:
    '''
    Converts a cif file to a POSCAR file.
    '''
    _s = structure.Structure(filename)
    _s.CIF_reader()
    _s.write_poscar()

def qm_region(filename: str, atom: str):
    '''
    Generates a qm region for a non-molecular crystal
    '''
    _s = structure.Structure(filename)
    _s.Vasp_reader()
    _s._find_index(atom)
    _s.Const_shift(_s.vector)
    _s.Supercell([2, 2, 2])
    _s._type = 'Cartesian'
    _s.Const_shift(-np.array([0.5, 0.5, 0.5]))
    _s.Cart_coords()
    _s._build_region()
    _s.write_xyz()

    

def Ewald(
        filename: str,
        qm_region: str,
        charges: str,
        atom: str,
        n: list,
        expansion: np.ndarray,
        r_cut: float,
        bound: float,
        verbose: int,
        ) -> None:
    '''
    Generates a xfield input file for molcas calulations using the Ewald summation.
    '''
    if 'csf' in socket.gethostname() and 'login' in socket.gethostname():
        raise Warning('DO NOT run ewald on the CSF login node!!!')
    _e = ewald.Ewald(
            qm_region,
            filename,
            charges,
            atom,
            n,
            r_cut,
            expansion,
            bound,
            verbose
            )
    _e.Calculate_Ewald()
    _e.Create_Zones()
    _e.Fitting()

def potential_plot(
        filename: str,
        xy_grid: int,
        n_points: int,
        n_contours: int,
        ) -> None:
    '''
    Generates a potential plot from a molcas xfield output file.
    '''
    pot = ewald.Potential(filename, xy_grid, n_points, n_contours)
    pot.Plot()

def create_input_configurations() -> None:
    '''
    Creates input configurations for VASP calculations.
    '''
    if not os.path.exists(os.path.expanduser('~/.vasp_suite_configs')):
        os.mkdir(os.path.expanduser('~/.vasp_suite_configs'))

    cwd = os.getcwd()
    os.chdir(os.path.expanduser('~/.vasp_suite_configs'))
    with open('relaxation.ini', 'w') as f:
        f.write('''[Relaxation]
prec = ACCURATE
lreal = .FALSE.
lasph = .TRUE.
ismear = 0
sigma = 0.1
nelm = 100
nelmin = 4
ncore = 4
ediff = 1e-08
ediffg = -0.01
ibrion = 2
nsw = 100
isif = 4
potim = 0.5
lwave = .FALSE.
lcharg = .FALSE.
lorbit = 11
gga = PE
ivdw = 11
''')
    with open('scf.ini', 'w') as f:
        f.write('''[SCF] 
                prec = ACCURATE
lreal = .FALSE.
lasph = .TRUE.
ismear = 0
sigma = 0.1
nelm = 100
nelmin = 4
ncore = 4
ediff = 1e-08
ediffg = -0.01
ibrion = -1
isif = 4
potim = 0.5
lwave = .FALSE.
lcharg = .FALSE.
lorbit = 11
gga = PE
ivdw = 11
''')
    os.chdir(cwd)
