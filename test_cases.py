import pytest
import os
from case import TestCase
from pathlib import Path

CASE_DIR = Path(__file__).parent / "cases"


@pytest.fixture
def pm():
    from napari.plugins import plugin_manager

    plugin_manager.discover()

    def _provides(plugin_name, hookspec_name):
        plugin = plugin_manager._ensure_plugin(plugin_name)
        return any(
            impl.plugin_name == plugin_manager.get_name(plugin)
            for impl in getattr(plugin_manager.hook, hookspec_name).get_hookimpls()
        )

    plugin_manager.provides = _provides
    return plugin_manager


def test_discovery(pm):
    # each filename stem in `cases` will be run as an independent tox env
    case_name = os.getenv("TOX_ENV_NAME")
    assert case_name

    case_file = next(f for f in CASE_DIR.glob("*.[y|ya]ml") if f.stem == case_name)
    assert case_file.exists()

    case = TestCase.from_file(case_file)
    for plugin in case.plugins:
        assert plugin.name in pm.plugins
        for hook in plugin.hooks:
            assert pm.provides(plugin.name, hook)
