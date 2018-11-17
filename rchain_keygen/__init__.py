
__version__ = '0.0.1'
# __version__ = '0.0.2'

SECONDS_TO_CHECK_PROCESS = 30
MAX_LINE_COLS = 79


class RNodeOptions:
    _BINARY_NAME = 'rnode'
    STANDALONE = '--standalone'
    NUMBER_OF_VALIDATORS = '--num-validators'
    DATA_DIRECTORY = '--data_dir'

    def __init__(self):
        self._idx = 0
        self._attrs = [element for element in dir(self) if not element.startswith('_')]

    def __iter__(self):
        return self

    def __next__(self):
        try:
            item_name = self._attrs[self._idx]
        except IndexError:
            raise StopIteration()
        else:
            self._idx += 1
            return getattr(self, item_name)
