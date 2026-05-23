import os


class VMWriter:
    def __init__(self, output_path):
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        self._file = open(output_path, 'w', encoding='utf-8')

    def write_push(self, segment, index):
        self._file.write(f'push {segment} {index}\n')

    def write_pop(self, segment, index):
        self._file.write(f'pop {segment} {index}\n')

    def write_arithmetic(self, command):
        self._file.write(f'{command}\n')

    def write_label(self, label):
        self._file.write(f'label {label}\n')

    def write_goto(self, label):
        self._file.write(f'goto {label}\n')

    def write_if_goto(self, label):
        self._file.write(f'if-goto {label}\n')

    def write_call(self, name, n_args):
        self._file.write(f'call {name} {n_args}\n')

    def write_function(self, name, n_locals):
        self._file.write(f'function {name} {n_locals}\n')

    def write_return(self):
        self._file.write('return\n')

    def close(self):
        self._file.close()
