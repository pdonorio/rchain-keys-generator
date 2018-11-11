import argparse


def get_arguments():
    option = 'save-as-source'
    parser = argparse.ArgumentParser(
        description="RChain 'ed25519' signed keys generator"
    )
    parser.add_argument(
        '--' + option,
        dest='save_file',
        action='store_true',
        help="enable saving variables for bash env sourcing",
    )
    # parser.add_argument('--no-' + option, dest='save_file', action='store_false')
    parser.set_defaults(save_file=False)
    return parser.parse_args()
