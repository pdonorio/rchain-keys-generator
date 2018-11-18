
__version__ = '0.0.1'
# __version__ = '0.0.2'

SECONDS_TO_CHECK_PROCESS = 30
MAX_LINE_COLS = 79


class RNodeOptions:

    _binary_name = 'rnode'
    _options = {
        'standalone': "standalone",
        'number_of_validators': "num_validators",
        'data_directory': "data_dir",
        'help': "help",
    }

    def __init__(self):
        print("TEST")
        pass

    @property
    def binary(self):
        return self._binary_name

    def fix_option(self, name):
        if name not in self._options:
            return False
        else:
            self._options[name] = self._options[name].replace('_', '-')
            return True

    def get_option(self, name):
        if name not in self._options:
            return None
        return '--' + self._options.get(name)

    def get_set_of_current_options(self):
        import re
        import subprocess
        raw = subprocess.check_output([self.binary, self.get_option('help')])
        output = raw.decode().replace('\n', '')
        regex = re.compile(r'--[^\s]+')
        all_options = regex.findall(output)
        self._all_options_set = set(all_options)

    def validate_options():
        print('Validating')
        pass
