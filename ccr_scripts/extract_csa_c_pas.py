from ccr_scripts.save_utils import save_csa_c_pas
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract PAS CSA C vectors')
    parser.add_argument('--path-to-CO-vectors')
    parser.add_argument('--path-to-C-CA-vectors')
    parser.add_argument('--output-directory', default=".")
    args = parser.parse_args()

    save_csa_c_pas(args.path_to_CO_vectors, args.path_to_C_CA_vectors, args.output_directory)
