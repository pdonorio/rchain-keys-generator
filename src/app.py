
import os
import time
import shutil
import subprocess
import threading

NODE_BINARY = 'rnode'
DATA_DIR = '/tmp/rnode_validator_keys'


def output_reader(proc):
    for line in iter(proc.stdout.readline, b''):
        line_string = line.decode('utf-8').lower()
        print('OUT: %s' % line_string, end='')
        if 'genesis' in line_string:
            if 'created validator' in line_string:
                proc.terminate()
                print("FINISHED!")


def proc_wait(proc):
    while True:
        still_running = proc.poll() is None
        if still_running:
            print("Node running:", still_running)
            time.sleep(1)
        else:
            break


def make_sure_process_is_closed(proc):
    proc.terminate()
    try:
        proc.wait(timeout=0.2)
        print('Process return code: ', proc.returncode)
    except subprocess.TimeoutExpired:
        print('Process did not terminate in time')


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


def run_all_threads(args):
    t1 = threading.Thread(target=output_reader, args=args)
    t2 = threading.Thread(target=proc_wait, args=args)
    t1.start() or t2.start()
    t1.join() or t2.join()


def main():
    remove_existing_data(DATA_DIR)
    proc = run_process(build_command(NODE_BINARY, DATA_DIR))
    args = (proc,)
    run_all_threads(args)
    make_sure_process_is_closed(*args)


if __name__ == '__main__':
    main()
