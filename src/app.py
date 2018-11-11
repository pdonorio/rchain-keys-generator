
import os
import time
import shutil
import argparse
import threading
import subprocess

SECONDS_TO_CHECK_PROCESS = 30
MAX_LINE_COLS = 79
NODE_BINARY = 'rnode'
CURRENT_WORKING_DIR = os.getcwd()


def get_arguments():
    option = 'save-as-source'
    parser = argparse.ArgumentParser(
        description="RChain 'ed25519' signed keys generator")
    parser.add_argument(
        '--' + option,
        dest='save_file', action='store_true',
        help="enable saving variables for bash env sourcing"
    )
    # parser.add_argument('--no-' + option, dest='save_file', action='store_false')
    parser.set_defaults(save_file=False)
    return parser.parse_args()


def end_proc_if_genesis(proc):

    line_number = 0
    for line in iter(proc.stdout.readline, b''):
        line_number += 1
        line_string = line.decode('utf-8').lower()
        line_stripped = line_string.split('[main]').pop().strip()
        running_output = 'RUNNING (line %s): %s' % (line_number, line_stripped)
        print(running_output[:MAX_LINE_COLS] + '\r', end='')

        if 'genesis' in line_string:
            if 'created validator' in line_string:
                proc.terminate()
                print('.' * MAX_LINE_COLS)
                print("\nCompleted\n")
        else:
            # show fast lines progress to human eye
            time.sleep(0.3)


def alert_for_longer_proc(proc):
    seconds = 0
    while True:
        seconds += 1
        if proc.poll() is None:
            time.sleep(1)
            if seconds % SECONDS_TO_CHECK_PROCESS == 0:
                output = "Warning: node still running after %s seconds" % seconds
                output += (MAX_LINE_COLS - len(output)) * '.'
                print(output)
        else:
            break


def make_sure_process_is_closed(proc):
    proc.terminate()
    try:
        proc.wait(timeout=0.2)
        # print('Process return code: ', proc.returncode)
    except subprocess.TimeoutExpired:
        pass
        # print('Process did not terminate in time')


def remove_existing_data(dir):
    if os.path.exists(dir) and os.path.isdir(dir):
        shutil.rmtree(dir)


def choose_data_dir(data_dir):
    if data_dir is None:
        from tempfile import TemporaryDirectory
        data_dir = TemporaryDirectory(prefix='rchain_').name
        print("Temporary dir: ", data_dir)
    else:
        remove_existing_data(data_dir)
    return data_dir


def build_command(data_dir, node_bin=NODE_BINARY):
    print("Launching: %s.\n" % node_bin)
    return [
        node_bin, 'run', '--standalone',
        '--num-validators', '1',
        '--data_dir', data_dir,
    ]


def run_process(command):
    return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def run_all_threads(functions, args):
    threads = []
    for function in functions:
        t = threading.Thread(target=function, args=args)
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()


def find_keyfile(current_data_dir):
    from glob import glob
    path_to_look = os.path.join(current_data_dir, 'genesis', '*sk')
    files = glob(path_to_look)
    if len(files) != 1:
        raise FileNotFoundError("Failed to find " + path_to_look)
    return files.pop()


def copy_keyfile_to_working_dir(original_keyfile_path):
    keyfile_name = os.path.basename(original_keyfile_path)
    dest_path = os.path.join(CURRENT_WORKING_DIR, keyfile_name)
    shutil.copy(original_keyfile_path, dest_path)
    assert os.path.exists(dest_path)
    assert os.path.isfile(dest_path)
    print('Generated %s\n(in current dir %s)' % (keyfile_name, CURRENT_WORKING_DIR))
    return dest_path


def read_and_print_keys(keyfile, save_as_file=False):
    pub_key = os.path.basename(keyfile).replace('.sk', '')
    with open(keyfile) as keyfile_handler:
        priv_key = keyfile_handler.read().strip()
    pub_string = "VALIDATOR_PUBLIC_KEY=%s" % pub_key
    priv_string = "VALIDATOR_PRIVATE_KEY=%s" % priv_key
    print('\n' + pub_string + '\n' + priv_string + '\n')

    if save_as_file:
        filename = 'rchain.validator_keys.sh'
        with open(os.path.join(CURRENT_WORKING_DIR, filename), 'w') as file_handler:
            content = "export %s\nexport %s\n" % (pub_string, priv_string)
            file_handler.write(content)
        print("Saved: %s\n" % filename)

        print("You can use it with:")
        print("$ source %s" % filename)
        print("$ env | grep -i validator")
        print()


def main(save_file=False, data_dir=None):

    current_data_dir = choose_data_dir(data_dir)
    proc = run_process(build_command(current_data_dir))

    args = (proc,)
    run_all_threads(functions=[end_proc_if_genesis, alert_for_longer_proc], args=args)
    make_sure_process_is_closed(*args)

    signed_key_path = copy_keyfile_to_working_dir(find_keyfile(current_data_dir))
    remove_existing_data(current_data_dir)
    read_and_print_keys(signed_key_path, save_as_file=save_file)


if __name__ == '__main__':
    args = get_arguments()
    main(save_file=args.save_file)
    # main(data_dir='/tmp/rnode_validator_keys')
