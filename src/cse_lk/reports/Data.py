import os
from functools import cached_property

from utils import Log, TSVFile

log = Log('Data')


class Data:
    def clean(self, x):
        return x

    @cached_property
    def data(self):
        raise NotImplementedError

    @property
    def data_file_path(self):
        return os.path.join('data', f'{self.__class__.__name__}.tsv')

    @property
    def data_file(self):
        return TSVFile(self.data_file_path)

    def store(self):
        self.data_file.write(self.data)
        log.info(f'Stored data to {self.data_file_path}')

    def load(self):
        if not self.data_file.exists:
            self.store()
        return [self.clean(x) for x in self.data_file.read()]
