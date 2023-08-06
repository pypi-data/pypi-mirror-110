import ast
import os
from functools import partial

from tryceratops import analyzers
from tryceratops.violations import Violation, codes


def read_sample(filename: str) -> ast.AST:
    ref_dir = f"{os.path.dirname(__file__)}/samples/violations/"
    path = f"{ref_dir}{filename}.py"

    with open(path) as sample:
        content = sample.read()
        loaded = ast.parse(content)
        return loaded


def assert_violation(code: str, msg: str, line: int, col: int, violation: Violation):
    assert violation.line == line
    assert violation.col == col
    assert violation.code == code
    assert violation.description == msg


def test_too_many_calls():
    tree = read_sample("call_too_many_try")
    analyzer = analyzers.CallTooManyAnalyzer()
    expected_code, expected_msg = codes.TOO_MANY_TRY
    assert_too_many = partial(assert_violation, expected_code, expected_msg)

    violations = analyzer.check(tree, "filename")

    assert len(violations) == 3
    v2blocks, v3blocks_1, v3blocks_2 = violations

    assert_too_many(15, 4, v2blocks)
    assert_too_many(27, 4, v3blocks_1)
    assert_too_many(32, 4, v3blocks_2)


def test_raise_vanilla():
    tree = read_sample("call_raise_vanilla")
    analyzer = analyzers.CallRaiseVanillaAnalyzer()

    assert_args = partial(
        assert_violation, codes.RAISE_VANILLA_ARGS[0], codes.RAISE_VANILLA_ARGS[1]
    )
    assert_class = partial(
        assert_violation, codes.RAISE_VANILLA_CLASS[0], codes.RAISE_VANILLA_CLASS[1]
    )

    violations = analyzer.check(tree, "filename")

    assert len(violations) == 2
    class_vio, args_vio = violations

    assert_class(13, 8, class_vio)
    assert_args(13, 8, args_vio)


def test_check_continue():
    tree = read_sample("call_check_continue")
    analyzer = analyzers.CallAvoidCheckingToContinueAnalyzer()
    msg = codes.CHECK_TO_CONTINUE[1].format("another_func")

    assert_check = partial(assert_violation, codes.CHECK_TO_CONTINUE[0], msg)

    violations = analyzer.check(tree, "filename")

    assert len(violations) == 2
    first, second = violations

    assert_check(20, 4, first)
    assert_check(24, 4, second)


def test_reraise_no_cause():
    tree = read_sample("except_reraise_no_cause")
    analyzer = analyzers.ExceptReraiseWithoutCauseAnalyzer()
    code, msg = codes.RERAISE_NO_CAUSE

    assert_no_cause = partial(assert_violation, code, msg)

    violations = analyzer.check(tree, "filename")
    assert len(violations) == 1

    assert_no_cause(16, 8, violations[0])


def test_verbose_reraise():
    tree = read_sample("except_verbose_reraise")
    analyzer = analyzers.ExceptVerboseReraiseAnalyzer()
    code, msg = codes.VERBOSE_RERAISE

    assert_verbose = partial(assert_violation, code, msg)

    violations = analyzer.check(tree, "filename")
    assert len(violations) == 2
    first, second = violations

    assert_verbose(20, 8, first)
    assert_verbose(28, 12, second)
