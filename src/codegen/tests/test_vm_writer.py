import os
import tempfile
import pytest
from src.codegen.VMWriter import VMWriter


def make_writer():
    fd, path = tempfile.mkstemp(suffix='.vm')
    os.close(fd)
    return VMWriter(path), path


def read_vm(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


class TestVMWriter:
    def test_push_constant(self):
        w, p = make_writer()
        w.write_push('constant', 5)
        w.close()
        assert read_vm(p) == 'push constant 5\n'

    def test_push_local(self):
        w, p = make_writer()
        w.write_push('local', 2)
        w.close()
        assert read_vm(p) == 'push local 2\n'

    def test_pop_local(self):
        w, p = make_writer()
        w.write_pop('local', 1)
        w.close()
        assert read_vm(p) == 'pop local 1\n'

    def test_pop_this(self):
        w, p = make_writer()
        w.write_pop('this', 0)
        w.close()
        assert read_vm(p) == 'pop this 0\n'

    def test_arithmetic_add(self):
        w, p = make_writer()
        w.write_arithmetic('add')
        w.close()
        assert read_vm(p) == 'add\n'

    def test_arithmetic_sub(self):
        w, p = make_writer()
        w.write_arithmetic('sub')
        w.close()
        assert read_vm(p) == 'sub\n'

    def test_arithmetic_neg(self):
        w, p = make_writer()
        w.write_arithmetic('neg')
        w.close()
        assert read_vm(p) == 'neg\n'

    def test_arithmetic_not(self):
        w, p = make_writer()
        w.write_arithmetic('not')
        w.close()
        assert read_vm(p) == 'not\n'

    def test_arithmetic_eq(self):
        w, p = make_writer()
        w.write_arithmetic('eq')
        w.close()
        assert read_vm(p) == 'eq\n'

    def test_arithmetic_lt(self):
        w, p = make_writer()
        w.write_arithmetic('lt')
        w.close()
        assert read_vm(p) == 'lt\n'

    def test_arithmetic_gt(self):
        w, p = make_writer()
        w.write_arithmetic('gt')
        w.close()
        assert read_vm(p) == 'gt\n'

    def test_label(self):
        w, p = make_writer()
        w.write_label('WHILE_START_0')
        w.close()
        assert read_vm(p) == 'label WHILE_START_0\n'

    def test_goto(self):
        w, p = make_writer()
        w.write_goto('LOOP_START')
        w.close()
        assert read_vm(p) == 'goto LOOP_START\n'

    def test_if_goto(self):
        w, p = make_writer()
        w.write_if_goto('IF_FALSE_0')
        w.close()
        assert read_vm(p) == 'if-goto IF_FALSE_0\n'

    def test_call(self):
        w, p = make_writer()
        w.write_call('Math.abs', 1)
        w.close()
        assert read_vm(p) == 'call Math.abs 1\n'

    def test_call_zero_args(self):
        w, p = make_writer()
        w.write_call('Memory.alloc', 1)
        w.close()
        assert read_vm(p) == 'call Memory.alloc 1\n'

    def test_function(self):
        w, p = make_writer()
        w.write_function('Main.main', 0)
        w.close()
        assert read_vm(p) == 'function Main.main 0\n'

    def test_function_with_locals(self):
        w, p = make_writer()
        w.write_function('Main.main', 3)
        w.close()
        assert read_vm(p) == 'function Main.main 3\n'

    def test_return(self):
        w, p = make_writer()
        w.write_return()
        w.close()
        assert read_vm(p) == 'return\n'

    def test_multiple_instructions_in_order(self):
        w, p = make_writer()
        w.write_push('constant', 5)
        w.write_push('constant', 3)
        w.write_arithmetic('add')
        w.write_call('Output.printInt', 1)
        w.write_pop('temp', 0)
        w.close()
        expected = (
            'push constant 5\n'
            'push constant 3\n'
            'add\n'
            'call Output.printInt 1\n'
            'pop temp 0\n'
        )
        assert read_vm(p) == expected
