# pylint: disable=missing-module-docstring
from saltrewrite.testsuite import fix_asserts
from saltrewrite.testsuite import fix_destructive_test_decorator
from saltrewrite.testsuite import fix_expensive_test_decorator
from saltrewrite.testsuite import fix_requires_network_decorator
from saltrewrite.testsuite import fix_requires_salt_modules_decorator
from saltrewrite.testsuite import fix_requires_salt_states_decorator
from saltrewrite.testsuite import fix_skip_if_binaries_missing_decorator
from saltrewrite.testsuite import fix_skip_if_not_root_decorator
from saltrewrite.testsuite import fix_slow_test_decorator

__all__ = [modname for modname in list(globals()) if modname.startswith("fix_")]

__fixes__ = [
    (getattr(module, "FIX_PRIORITY", 0), module)
    for module in [globals()[modname] for modname in __all__]
]
