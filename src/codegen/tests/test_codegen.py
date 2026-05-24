import os
import tempfile
import pytest
from pathlib import Path
from src.scanner.Scanner import Scanner
from src.codegen.CodeGenerator import CodeGenerator

TESTS_DIR = Path(__file__).parent
INPUTS_DIR = TESTS_DIR / 'inputs'
EXPECTED_DIR = TESTS_DIR / 'expected'


def compile_to_string(jack_path: Path) -> str:
    fd, tmp = tempfile.mkstemp(suffix='.vm')
    os.close(fd)
    scanner = Scanner(str(jack_path))
    scanner.tokenizar()
    tokens = scanner.get_tokens()
    gen = CodeGenerator(tokens, tmp)
    gen.compile()
    with open(tmp, encoding='utf-8') as f:
        return f.read()


def load_expected(name: str) -> str:
    return (EXPECTED_DIR / name).read_text(encoding='utf-8')


def lines(text: str) -> list[str]:
    return [l for l in text.splitlines() if l.strip()]


# ------------------------------------------------------------------ unit-style


class TestExpressions:
    """Operações aritméticas, variáveis locais e de argumento."""

    def test_function_header(self):
        out = compile_to_string(INPUTS_DIR / 'expressions.jack')
        assert lines(out)[0] == 'function Expressions.compute 1'

    def test_args_pushed_for_addition(self):
        out = compile_to_string(INPUTS_DIR / 'expressions.jack')
        ls = lines(out)
        assert 'push argument 0' in ls
        assert 'push argument 1' in ls

    def test_result_stored_in_local(self):
        out = compile_to_string(INPUTS_DIR / 'expressions.jack')
        assert 'pop local 0' in lines(out)

    def test_result_returned_from_local(self):
        out = compile_to_string(INPUTS_DIR / 'expressions.jack')
        ls = lines(out)
        idx_push = next(i for i, l in enumerate(ls) if l == 'push local 0')
        assert ls[idx_push + 1] == 'return'

    def test_full_output_matches_expected(self):
        out = compile_to_string(INPUTS_DIR / 'expressions.jack')
        assert lines(out) == lines(load_expected('expressions.vm'))


class TestControlFlow:
    """if/else com labels únicos e numerados."""

    def test_function_header(self):
        out = compile_to_string(INPUTS_DIR / 'control.jack')
        assert lines(out)[0] == 'function Control.max 0'

    def test_condition_uses_gt(self):
        out = compile_to_string(INPUTS_DIR / 'control.jack')
        assert 'gt' in lines(out)

    def test_condition_negated_before_branch(self):
        out = compile_to_string(INPUTS_DIR / 'control.jack')
        ls = lines(out)
        idx_gt = ls.index('gt')
        assert ls[idx_gt + 1] == 'not'

    def test_if_false_label_exists(self):
        out = compile_to_string(INPUTS_DIR / 'control.jack')
        assert 'label IF_FALSE_0' in lines(out)

    def test_if_end_label_exists(self):
        out = compile_to_string(INPUTS_DIR / 'control.jack')
        assert 'label IF_END_0' in lines(out)

    def test_full_output_matches_expected(self):
        out = compile_to_string(INPUTS_DIR / 'control.jack')
        assert lines(out) == lines(load_expected('control.vm'))


class TestArrays:
    """Atribuição a array: padrão temp/pointer/that."""

    def test_function_header(self):
        out = compile_to_string(INPUTS_DIR / 'arrays.jack')
        assert lines(out)[0] == 'function Arrays.set 0'

    def test_array_base_pushed(self):
        out = compile_to_string(INPUTS_DIR / 'arrays.jack')
        assert 'push argument 0' in lines(out)

    def test_index_zero_pushed(self):
        out = compile_to_string(INPUTS_DIR / 'arrays.jack')
        assert 'push constant 0' in lines(out)

    def test_address_computed_with_add(self):
        out = compile_to_string(INPUTS_DIR / 'arrays.jack')
        assert 'add' in lines(out)

    def test_value_saved_to_temp_before_pointer(self):
        out = compile_to_string(INPUTS_DIR / 'arrays.jack')
        ls = lines(out)
        idx = ls.index('pop temp 0')
        assert ls[idx + 1] == 'pop pointer 1'

    def test_value_restored_and_stored_via_that(self):
        out = compile_to_string(INPUTS_DIR / 'arrays.jack')
        ls = lines(out)
        idx = ls.index('pop pointer 1')
        assert ls[idx + 1] == 'push temp 0'
        assert ls[idx + 2] == 'pop that 0'

    def test_full_output_matches_expected(self):
        out = compile_to_string(INPUTS_DIR / 'arrays.jack')
        assert lines(out) == lines(load_expected('arrays.vm'))


class TestClasses:
    """Constructor (Memory.alloc + pointer 0) e method (arg 0 → pointer 0)."""

    def test_constructor_header(self):
        out = compile_to_string(INPUTS_DIR / 'classes.jack')
        assert 'function Counter.new 0' in lines(out)

    def test_constructor_allocates_fields(self):
        out = compile_to_string(INPUTS_DIR / 'classes.jack')
        ls = lines(out)
        assert 'push constant 1' in ls
        assert 'call Memory.alloc 1' in ls

    def test_constructor_sets_pointer_zero(self):
        out = compile_to_string(INPUTS_DIR / 'classes.jack')
        ls = lines(out)
        idx = ls.index('call Memory.alloc 1')
        assert ls[idx + 1] == 'pop pointer 0'

    def test_constructor_returns_this(self):
        out = compile_to_string(INPUTS_DIR / 'classes.jack')
        ls = lines(out)
        # primeiro 'return' deve ser precedido por 'push pointer 0'
        idx_ret = ls.index('return')
        assert ls[idx_ret - 1] == 'push pointer 0'

    def test_method_header(self):
        out = compile_to_string(INPUTS_DIR / 'classes.jack')
        assert 'function Counter.get 0' in lines(out)

    def test_method_sets_this_from_arg0(self):
        out = compile_to_string(INPUTS_DIR / 'classes.jack')
        ls = lines(out)
        idx = ls.index('function Counter.get 0')
        assert ls[idx + 1] == 'push argument 0'
        assert ls[idx + 2] == 'pop pointer 0'

    def test_method_reads_field_via_this(self):
        out = compile_to_string(INPUTS_DIR / 'classes.jack')
        ls = lines(out)
        idx = ls.index('function Counter.get 0')
        # após o prologue (push arg0, pop pointer 0) deve vir push this 0
        assert 'push this 0' in ls[idx:]

    def test_full_output_matches_expected(self):
        out = compile_to_string(INPUTS_DIR / 'classes.jack')
        assert lines(out) == lines(load_expected('classes.vm'))


# ----------------------------------------------------------------- project 11


PROJECT11 = [
    ('Seven',         'input/Seven/Main.jack'),
    ('Average',       'input/Average/Main.jack'),
    ('ConvertToBin',  'input/ConvertToBin/Main.jack'),
    ('ComplexArrays', 'input/ComplexArrays/Main.jack'),
]

ROOT = Path(__file__).parent.parent.parent.parent  # raiz do projeto


@pytest.mark.parametrize('name,jack_rel', PROJECT11)
def test_project11_compiles_without_error(name, jack_rel):
    """Verifica que o compilador não lança exceção nos programas do Project 11."""
    jack_path = ROOT / jack_rel
    if not jack_path.exists():
        pytest.skip(f'{jack_path} não encontrado')
    compile_to_string(jack_path)


@pytest.mark.parametrize('name,jack_rel', PROJECT11)
def test_project11_output_matches_reference(name, jack_rel):
    """Compara o VM gerado com o arquivo .vm de referência já existente."""
    jack_path = ROOT / jack_rel
    vm_ref_path = jack_path.with_suffix('.vm')
    if not jack_path.exists() or not vm_ref_path.exists():
        pytest.skip(f'arquivos de referência não encontrados para {name}')
    out = compile_to_string(jack_path)
    ref = vm_ref_path.read_text(encoding='utf-8')
    assert lines(out) == lines(ref)
