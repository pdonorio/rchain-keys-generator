from rchain_keygen import app
from rchain_keygen.arguments import get_arguments


def main():

    parsed_args = get_arguments()
    data_dir = app.choose_data_dir()
    command = app.build_command(data_dir)
    proc = app.run_process(command)

    ######
    args = (proc,)
    app.run_all_threads(
        functions=[app.end_proc_if_genesis, app.alert_for_longer_proc], args=args
    )
    if app.make_sure_process_is_closed(*args):
        signed_key_path = app.copy_keyfile_to_working_dir(app.find_keyfile(data_dir))
        app.remove_existing_data(data_dir)
        app.read_and_print_keys(signed_key_path, save_as_file=parsed_args.save_file)


if __name__ == '__main__':
    main()
