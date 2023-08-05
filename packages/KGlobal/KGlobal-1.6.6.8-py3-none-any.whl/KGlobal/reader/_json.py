from ..filehandler import FileHandler
from json import loads
from portalocker import Lock
from pandas import DataFrame


class JSONReader(FileHandler):
    def __init__(self, file_path, **kwargs):
        super().__init__(file_path=file_path, **kwargs)

    def parse(self):
        if self.streams:
            for handler, buffer in self.streams:
                self.__parse(handler=handler, buffer=buffer)
        else:
            return self.__parse()

    def __parse(self, handler=None, buffer=None):
        data = list()
        row_num = 0
        header = None

        with Lock(filename=self.file_path, mode='r') as read_obj:
            for line in read_obj:
                data.append(loads(line))

                if not header:
                    header = converted_row

                if handler and buffer <= len(data):
                    handler(self.file_path, data, row_num - len(data) + 1, row_num, **self.kwargs)
                    data.clear()
                    data.append(header)

                row_num += 1

        if data and handler:
            row_num -= 1
            handler(self.file_path, data, row_num - len(data) + 1, row_num, **self.kwargs)
        elif not handler:
            return data

    @staticmethod
    def __to_df(data):
        if data:
            df = DataFrame(data)
            new_header = df.iloc[0]
            df = df[1:]
            df.columns = new_header
            return df
        else:
            return DataFrame()
