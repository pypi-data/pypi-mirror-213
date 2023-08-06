# Import argparse
import argparse
from textwrap import dedent
import numpy as np

# Import Modules
from . import core

# Create the wrapper funstions 

def generate_input_func(args):
    '''
    Wrapper function for the generate_input function

    parameters
    ----------
    filename : str
    config_file : file

    Returns
    -------
    INCAR : file
    '''
    core.generate_input(
        filename=args.filename,
        calculation=args.config_file,
            )

def calculate_kpoints_func(args):
    '''
    Wrapper function for the calculate_kpoints function

    parameters
    ----------
    filename : str

    Returns
    -------
    KPOINT mesh : int 
    '''
    core.calculate_kpoints(
            filename=args.filename,
            )

def generate_kpoints_func(args):
    '''
    Wrapper function for the generate_kpoints function 

    parameters
    ----------
    mesh : int 

    Returns
    -------
    KPOINTS : file
    '''
    core.generate_kpoints(
            mesh=args.mesh,
            )

def generate_supercell_func(args):
    '''
    Wrapper function for the generate_supercell function

    parameters
    ----------
    expansion : list

    Returns
    -------
    POSCAR : file 
    .xyz : file
    '''
    core.generate_supercell(
            expansion=np.array(args.expansion, dtype=int),
            )

def generate_job_func(args):
    '''
    Wrapper function for the generate_job function 

    parameters
    ----------
    title : str 
    cores : int 
    vasp_type : str 

    Returns
    -------
    job.sh : file
    '''
    core.generate_job(
            title=args.title,
            cores=args.cores,
            vasp_type=args.vasp_type,
            )

def start_up_func(args):
    '''
    Wrapper function for the start_up function

    parameters
    ----------
    None

    Returns
    -------
    configuration files : file
    '''
    core.create_input_configurations()

def dope_structure_func(args):
    '''
    Wrapper function for the dope_structure function

    parameters
    ----------
    filename : str 
    dopant : str 
    replace : str 
    instances : int 
    
    Returns
    -------
    POSCARs : file 
    '''
    core.dope_structure(
        filename=args.filename,
        dopant=args.dopant,
        replace=args.replace,
        instances=args.instances,
        )

def generate_defect_func(args): 
    '''
    Wrapper function for the generate_defect function

    parameters
    ----------
    filename : str 
    site : str 
    instances : int 

    Returns
    -------
    POSCAR : file 
    '''
    core.generate_defect(
            filename=args.filename,
            site=args.site,
            instances=args.instances,
            )

def asymmetric_unit_func(args):
    '''
    Wrapper function for the asymmetric_unit function

    parameters
    ----------
    filename : str 
    atom : str 
    bond_max : float 

    Returns
    -------
    POSCAR : file 
    '''
    core.asymmetric_unit(
            filename=args.filename,
            atom=args.atom,
            bond_max=args.bond_max,
            )

def Ewald_func(args):
    '''
    Wrapper function for the Ewald function

    parameters
    ----------
    qm_region : str 
    filename : str 
    charges : str 
    atom : str 
    n : list 
    r_cut : float 
    expansion : list 

    Returns 
    ------- 
    Ewald.out : file 
    '''
    core.Ewald(
            qm_region=args.qm_region,
            filename=args.filename,
            charges=args.charges,
            atom=args.atom,
            n=args.n,
            r_cut=args.r_cut,
            expansion=args.expansion,
            bound=0.0,
            verbose=args.verbose,
            )

def potential_plot_func(args):
    '''
    Wrapper function for the potential_plot function

    parameters
    ----------
    filename : str 
    xy_grid : int 
    n_points : int 
    n_contours : int

    Returns
    -------
    None
    '''
    core.potential_plot(
            filename=args.filename,
            xy_grid=args.xy_grid, 
            n_points=args.n_points, 
            n_contours=args.n_contours,
            )

def convert_cif_func(args):
    '''
    Wrapper function for the convert_cif function

    parameters
    ----------
    filename : str 

    Returns
    -------
    POSCAR : file 
    '''
    core.convert_cif(
            filename=args.filename,
            )

def qm_region_func(args):
    '''
    Wrapper function for the qm_region function

    parameters
    ----------
    filename : str 
    atom : str 
    r_cut : float 
    expansion : list 

    Returns
    -------
    POSCAR : file 
    '''
    core.qm_region(
            filename=args.filename,
            atom=args.atom,
            )

def read_args(arg_list=None):
    '''Reads the command line arguments'''
    parser = argparse.ArgumentParser(
            prog='vasp_suite',
            description=dedent(
                '''
                ---------------------------------------------------
                                                  
                      A suite of tools for VASP calculations      

                ---------------------------------------------------
                
                Available programmes:
                    vasp_suite generate_input ...
                    vasp_suite generate_job ...
                    vasp_suite calculate_kpoints ...
                    vasp_suite generate_kpoints ...
                    vasp_suite generate_supercell ...
                    vasp_suite convert_cif ...
                    vasp_suite start_up ...
                    vasp_suite dope_structure ...
                    vasp_suite generate_defect ...
                    vasp_suite molecular_qm ...
                    vasp_suite ewald ...
                    vasp_suite plot_potential ...
                    vasp_suite qm_region ...
                '''
                ),
            epilog=dedent(
                '''
                To display options for a specific programme, use vasp_suite <programme> -h
                '''
                ),
            formatter_class=argparse.RawDescriptionHelpFormatter
            )

    # Subparsers
    subparsers = parser.add_subparsers(dest='prog')

    gen_inp = subparsers.add_parser(
            'generate_input',
            help='Generate input files for VASP calculations',
            description=dedent(
                '''
                Generation of INCAR and POTCAR files for VASP calculations.
                '''
                ),
            formatter_class=argparse.RawDescriptionHelpFormatter
            )

    gen_inp.set_defaults(func=generate_input_func)

    gen_inp.add_argument(
            'config_file',
            help=dedent(
                '''
                The configuration file for the input generation.
                
                Example:
                Inside ~/.vasp_suite_templates '.ini' configuration files are 
                stored. To perform a relaxation caluclation using the relaxation.ini 
                template, use the following command:

                vasp_suite generate_input relaxation
                '''
                )
            )

    gen_inp.add_argument(
            '--filename', '-f',
            help=dedent(
                '''
                The name of the structure file, default is POSCAR
                '''
                ),
            default='POSCAR'
            )

    gen_job = subparsers.add_parser(
        'generate_job',
        help='Generate job submission files for VASP calculations',
        formatter_class=argparse.RawDescriptionHelpFormatter
        )

    gen_job.set_defaults(func=generate_job_func)

    gen_job.add_argument(
        'title',
        help='The title of the job'
        )

    gen_job.add_argument(
        'cores',
        help='The number of cores to use',
        type=int,
        )

    gen_job.add_argument(
        '--vasp_type',
        help=dedent(
            '''
            The VASP programme you widh to use:
                - vasp_std
                - vasp_gam
            '''
            ),
        default='vasp_gam'
        )

    calc_kpoints = subparsers.add_parser(
        'calculate_kpoints',
        help='Calculate the possible kpoint meshes for a given structure',
        formatter_class=argparse.RawDescriptionHelpFormatter
        )

    calc_kpoints.set_defaults(func=calculate_kpoints_func)

    calc_kpoints.add_argument(
            '--filename', '-f',
            help=dedent(
                '''
                The name of the structure file, default is POSCAR
                '''
                ),
            default='POSCAR'
            )

    gen_kpoints = subparsers.add_parser(
        'generate_kpoints',
        help='Generate the kpoints file for a given structure',
        formatter_class=argparse.RawDescriptionHelpFormatter
        )

    gen_kpoints.set_defaults(func=generate_kpoints_func)

    gen_kpoints.add_argument(
        'mesh',
        nargs=3,
        help=dedent(
            '''
            The mesh to use for the kpoints file.
            command line arguments are written in the form:
            a b c
            '''
            )
        )

    gen_supercell = subparsers.add_parser(
        'generate_supercell',
        help='Generate a supercell from a given structure',
        formatter_class=argparse.RawDescriptionHelpFormatter
        )

    gen_supercell.set_defaults(func=generate_supercell_func)

    gen_supercell.add_argument(
        'expansion',
        nargs=3,
        help=dedent(
            '''
            The expansion vector for the supercell, a b c
            '''
            ),
        )

    start_up = subparsers.add_parser(
        'set_up',
        help='Generate the configuration files for the suite',
        formatter_class=argparse.RawDescriptionHelpFormatter
        )

    start_up.set_defaults(func=start_up_func)

    dope_struct = subparsers.add_parser(
        'dope_structure',
        help='Dope a structure with a given element',
        formatter_class=argparse.RawDescriptionHelpFormatter
        )

    dope_struct.set_defaults(func=dope_structure_func)

    dope_struct.add_argument(
        '--filename', '-f',
        help='The name of the structure file',
        default='POSCAR',
        )

    dope_struct.add_argument(
            'dopant',
            help='The element to dope the structure with',
            )

    dope_struct.add_argument(
            'replace',
            help='The element to replace',
            ) 

    dope_struct.add_argument(
            '--instances',
            help='The number of instances of the dopant to add',
            type=int,
            default=1,
            )

    gen_defect = subparsers.add_parser(
        'generate_defect',
        help='Generate a defect structure',
        formatter_class=argparse.RawDescriptionHelpFormatter
        )

    gen_defect.set_defaults(func=generate_defect_func)

    gen_defect.add_argument(
            '--filename', '-f',
            help='The name of the structure file',
            default='POSCAR',
            )

    gen_defect.add_argument(
            'site',
            help='The name of the atom to remove',
            )

    gen_defect.add_argument(
            '--instances',
            help='The number of instances of defect',
            type=int,
            default=1,
            )

    asym = subparsers.add_parser(
        'molecular_qm',
        help='Generate the asymmetric unit of a structure',
        formatter_class=argparse.RawDescriptionHelpFormatter
        )

    asym.set_defaults(func=asymmetric_unit_func)

    asym.add_argument(
            '--filename', '-f',
            help='The name of the structure file',
            default='POSCAR',
            )

    asym.add_argument(
            'atom',
            help='The name of the spin centre in the molecular crystal',
            )

    asym.add_argument(
            '--bond_max', '-b',
            help='The maximum bond length/ Å',
            type=float,
            default=2.6,
            )

    ewald = subparsers.add_parser(
        'ewald',
        help='Calculate the ewald potential and fit paramaeter charges to the potential for electronic structure calculations',
        formatter_class=argparse.RawDescriptionHelpFormatter
        )

    ewald.set_defaults(func=Ewald_func)

    ewald.add_argument(
            '--filename', '-f',
            help='The name of the structure file',
            default='POSCAR',
            )

    ewald.add_argument(
            'qm_region',
            help='The name of the qm region, (.xyz file created using asymmetric unit)',
            )

    ewald.add_argument(
            'charges',
            help='The name of the file containing the charges',
            )

    ewald.add_argument(
            'atom',
            help='The name of the spin centre in the molecular crystal <Dy1>',
            )

    ewald.add_argument(
            '--n',
            help='The summation expansion',
            default= [3, 3, 3],
            nargs=3,
            type=int,
            )

    ewald.add_argument(
            'r_cut',
            help='The cutoff radius for the sphere region',
            type=float,
            )

    ewald.add_argument(
            'expansion',
            help='The expansion vector for the supercell, a b c',
            nargs=3,
            type=int,
            )

    ewald.add_argument(
            '--verbose', '-v',
            help='The level of verbosity in the fitting process\n0: No output\n1: Optimility and cost function\n2: Full output',
            default=1,
            type=int,
            )

    pot = subparsers.add_parser(
            'plot_potential',
            help='Plot the potential in the xy plane for a given mesh grid',
            formatter_class=argparse.RawDescriptionHelpFormatter
            )

    pot.set_defaults(func=potential_plot_func)

    pot.add_argument(
            '--filename', '-f',
            help='The name of the data file. delfault is ewald.out\n The layout of the file should be:\n x y z charge',
            default='ewald.out',
            )

    pot.add_argument(
            'xy_grid',
            help='The length in angstrom of the mesh grid in the xy plane. from -xy_grid to xy_grid',
            type=int,
            )

    pot.add_argument(
            '--n_points', '-p',
            help='The number of points in the mesh grid',
            type=int,
            default=50,
            )

    pot.add_argument(
            '--n_contours', '-c',
            help='The number of contours to plot',
            type=int,
            default=100,
            )

    cif = subparsers.add_parser(
            'convert_cif',
            help='Generate a cif file from a structure file',
            formatter_class=argparse.RawDescriptionHelpFormatter
            ) 

    cif.set_defaults(func=convert_cif_func) 

    cif.add_argument(
            'filename',
            help='The name of the .CIF file',
            )

    qm = subparsers.add_parser(
            'qm_region',
            help='Generate a .xyz file containing the qm region for non-molecular crystals',
            formatter_class=argparse.RawDescriptionHelpFormatter
            )

    qm.set_defaults(func=qm_region_func)

    qm.add_argument(
            '--filename', '-f',
            help='The name of the structure file',
            default='POSCAR',
            )

    qm.add_argument(
            'atom',
            help='The name of the spin centre in the crystal, <Dy1>',
            )


    # Parse the ArgumentParser
    parser.set_defaults(func=lambda args: parser.print_help())
    args = parser.parse_known_args(arg_list)

    # Select programme 
    if args in ['generate_input, generate_job, calculate_kpoints, generate_kpoints, generate_supercell, start_up, dope_structure, generate_defect, asymmetric_unit, ewald, plot_potential, convert_cif']:
        args.func(args)
    else:
        args = parser.parse_args(arg_list)
        args.func(args)

def main():
    read_args()
