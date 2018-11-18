import os
import time
import shutil
import threading
import subprocess
from rchain_keygen import MAX_LINE_COLS, SECONDS_TO_CHECK_PROCESS, RNodeOptions

CURRENT_WORKING_DIR = os.getcwd()


def invalid_option(single_line):
    return 'unknown option' in single_line


def end_proc_if_genesis(proc):

    line_number = 0
    for line in iter(proc.stdout.readline, b''):
        line_number += 1
        line_string = line.decode('utf-8').lower()
        line_stripped = line_string.split('[main]').pop().strip()

        if invalid_option(line_stripped):
            raise AttributeError("Failing option\n%s" % line_stripped)
        else:
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
        # print('Process did not terminate in time')
        return False
    else:
        if not RNodeOptions.accept_code(proc.returncode):
            print('Process failure')
            return False
    return True


def remove_existing_data(dir):
    if os.path.exists(dir) and os.path.isdir(dir):
        shutil.rmtree(dir)


def choose_data_dir(data_dir=None):
    if data_dir is None:
        from tempfile import TemporaryDirectory

        data_dir = TemporaryDirectory(prefix='rchain_').name
        print("Temporary dir: ", data_dir)
    else:
        remove_existing_data(data_dir)
    return data_dir


def build_command(data_dir):

    options = RNodeOptions()
    command = [
        options.binary,
        options.run,  # runner
        options.get_option('standalone'),  # standalone mode
        options.get_option('number_of_validators'),
        '1',  # avoid other validators
        options.get_option('data_directory'),
        data_dir,  # specify data directory
    ]
    return command


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
