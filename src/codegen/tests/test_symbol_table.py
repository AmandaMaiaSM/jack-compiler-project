import pytest
from src.codegen.SymbolTable import SymbolTable


@pytest.fixture
def sym():
    return SymbolTable()


class TestClassScope:
    def test_static_kind_and_segment(self, sym):
        sym.define('count', 'int', 'static')
        assert sym.kind_of('count') == 'static'
        assert sym.segment_of('count') == 'static'

    def test_static_type(self, sym):
        sym.define('count', 'int', 'static')
        assert sym.type_of('count') == 'int'

    def test_static_index_starts_at_zero(self, sym):
        sym.define('count', 'int', 'static')
        assert sym.index_of('count') == 0

    def test_field_segment_is_this(self, sym):
        sym.define('x', 'int', 'field')
        assert sym.segment_of('x') == 'this'

    def test_field_index_increments(self, sym):
        sym.define('x', 'int', 'field')
        sym.define('y', 'int', 'field')
        sym.define('z', 'int', 'field')
        assert sym.index_of('x') == 0
        assert sym.index_of('y') == 1
        assert sym.index_of('z') == 2

    def test_static_and_field_indices_are_independent(self, sym):
        sym.define('a', 'int', 'static')
        sym.define('b', 'int', 'field')
        sym.define('c', 'int', 'static')
        assert sym.index_of('a') == 0
        assert sym.index_of('b') == 0
        assert sym.index_of('c') == 1

    def test_var_count_field(self, sym):
        sym.define('x', 'int', 'field')
        sym.define('y', 'int', 'field')
        assert sym.var_count('field') == 2

    def test_var_count_static(self, sym):
        sym.define('x', 'int', 'static')
        assert sym.var_count('static') == 1

    def test_field_class_type(self, sym):
        sym.define('sq', 'Square', 'field')
        assert sym.type_of('sq') == 'Square'


class TestSubroutineScope:
    def test_function_arg_starts_at_zero(self, sym):
        sym.start_subroutine('function')
        sym.define('n', 'int', 'arg')
        assert sym.index_of('n') == 0

    def test_method_arg_starts_at_one(self, sym):
        sym.start_subroutine('method')
        sym.define('n', 'int', 'arg')
        assert sym.index_of('n') == 1

    def test_constructor_arg_starts_at_zero(self, sym):
        sym.start_subroutine('constructor')
        sym.define('n', 'int', 'arg')
        assert sym.index_of('n') == 0

    def test_arg_segment_is_argument(self, sym):
        sym.start_subroutine('function')
        sym.define('x', 'int', 'arg')
        assert sym.segment_of('x') == 'argument'

    def test_local_segment_is_local(self, sym):
        sym.start_subroutine('function')
        sym.define('x', 'int', 'local')
        assert sym.segment_of('x') == 'local'

    def test_local_index_increments(self, sym):
        sym.start_subroutine('function')
        sym.define('a', 'int', 'local')
        sym.define('b', 'int', 'local')
        assert sym.index_of('a') == 0
        assert sym.index_of('b') == 1

    def test_var_count_local(self, sym):
        sym.start_subroutine('function')
        sym.define('x', 'int', 'local')
        sym.define('y', 'int', 'local')
        assert sym.var_count('local') == 2


class TestScopeReset:
    def test_local_cleared_on_new_subroutine(self, sym):
        sym.start_subroutine('function')
        sym.define('x', 'int', 'local')
        sym.start_subroutine('function')
        assert sym.kind_of('x') == 'NONE'

    def test_local_count_resets(self, sym):
        sym.start_subroutine('function')
        sym.define('x', 'int', 'local')
        sym.define('y', 'int', 'local')
        sym.start_subroutine('function')
        assert sym.var_count('local') == 0

    def test_arg_count_resets_for_function(self, sym):
        sym.start_subroutine('method')
        sym.define('n', 'int', 'arg')
        sym.start_subroutine('function')
        assert sym.var_count('arg') == 0

    def test_class_scope_persists_across_subroutines(self, sym):
        sym.define('count', 'int', 'static')
        sym.start_subroutine('function')
        assert sym.kind_of('count') == 'static'
        assert sym.index_of('count') == 0

    def test_field_persists_across_subroutines(self, sym):
        sym.define('x', 'int', 'field')
        sym.start_subroutine('method')
        sym.start_subroutine('function')
        assert sym.kind_of('x') == 'field'


class TestLookupPriority:
    def test_local_shadows_field(self, sym):
        sym.define('x', 'int', 'field')
        sym.start_subroutine('function')
        sym.define('x', 'boolean', 'local')
        assert sym.kind_of('x') == 'local'
        assert sym.type_of('x') == 'boolean'
        assert sym.segment_of('x') == 'local'

    def test_unknown_symbol_kind_is_none(self, sym):
        assert sym.kind_of('undefined') == 'NONE'

    def test_unknown_symbol_type_is_none(self, sym):
        assert sym.type_of('undefined') is None

    def test_unknown_symbol_index_is_none(self, sym):
        assert sym.index_of('undefined') is None

    def test_unknown_symbol_segment_is_none(self, sym):
        assert sym.segment_of('undefined') is None
