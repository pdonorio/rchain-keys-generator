import re
import subprocess

__version__ = '0.0.2'

SECONDS_TO_CHECK_PROCESS = 30
MAX_LINE_COLS = 79


class RNodeOptions:

    _codes = {'valid': 0, 'interrupted': 143}
    _binary_name = 'rnode'
    _run_command = 'run'
    _options = {
        'standalone': "standalone",
        'number_of_validators': "num_validators",
        'data_directory': "data_dir",
        'help': "help",
    }

    def __init__(self):
        self.get_set_of_current_options()
        self.validate_options()

    @property
    def binary(self):
        return self._binary_name

    @property
    def run(self):
        return self._run_command

    @classmethod
    def accept_code(cls, return_code):
        return return_code == cls.get_code('valid') or return_code == cls.get_code(
            'interrupted'
        )

    @classmethod
    def get_code(cls, name):
        if name not in cls._codes:
            return None
        else:
            return cls._codes.get(name)

    def get_option(self, name):
        if name not in self._options:
            return None
        else:
            return '--' + self._options.get(name)

    def get_set_of_current_options(self):
        print('Verifying node options')
        raw = subprocess.check_output([self.binary, self.get_option('help')])
        output = raw.decode().replace('\n', '')
        regex = re.compile(r'--[^\s]+')
        all_options = regex.findall(output)
        self._all_options_set = set(all_options)

    def validate_options(self):
        print('Validating')
        validated_options = {}
        for name, value in self._options.items():
            if self.get_option(name) not in self._all_options_set:
                # backwards compatibility
                value = value.replace('_', '-')
            validated_options[name] = value
        self._options = validated_options
