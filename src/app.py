
# import time
import subprocess
import threading

DATA_DIR = '/tmp/rnode_validator_keys'


def output_reader(proc):
    for line in iter(proc.stdout.readline, b''):
        line_string = line.decode('utf-8').lower()
        print('OUT: %s' % line_string, end='')
        if 'genesis' in line_string:
            if 'created validator' in line_string:
                proc.terminate()
                print("FINISHED!")


def make_sure_process_is_closed(proc):
    proc.terminate()
    try:
        proc.wait(timeout=0.2)
        print('== subprocess exited with rc =', proc.returncode)
    except subprocess.TimeoutExpired:
        print('subprocess did not terminate in time')


def main():
    command = [
        'rnode', 'run',
        '--standalone',
        '--num-validators', '1',
        '--data_dir', DATA_DIR,
    ]
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # TODO: add second thread to check proc status and warn every 30s
    t = threading.Thread(target=output_reader, args=(proc,))
    t.start()
    t.join()


if __name__ == '__main__':
    main()
