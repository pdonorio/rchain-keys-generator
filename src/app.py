
import os
import time
import shutil
import subprocess
import threading

MAX_LINE_COLS = 79
NODE_BINARY = 'rnode'
DATA_DIR = '/tmp/rnode_validator_keys'


def output_reader(proc):

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


def proc_wait(proc):
    seconds = 0
    while True:
        seconds += 1
        if proc.poll() is None:
            time.sleep(1)
            if seconds % 30 == 0:
                print("Warning: node still running after %s seconds" % seconds)
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


def build_command(node_bin, data_dir):
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


def main():
    remove_existing_data(DATA_DIR)
    proc = run_process(build_command(NODE_BINARY, DATA_DIR))
    print("RNode launched.\n")
    args = (proc,)
    functions = [output_reader, proc_wait]
    run_all_threads(functions, args)
    make_sure_process_is_closed(*args)


if __name__ == '__main__':
    main()
