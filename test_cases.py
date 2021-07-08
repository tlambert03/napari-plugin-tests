import os
from pathlib import Path
from napari.plugins._plugin_manager import NapariPluginManager
from napari._qt.widgets.qt_viewer_dock_widget import QDockWidget
from napari import Viewer

import pytest

from case import TestCase as TC


@pytest.fixture
def pm():
    from napari.plugins import plugin_manager

    plugin_manager.discover()
    plugin_manager.discover_widgets()
    plugin_manager.discover_sample_data()

    def _provides(plugin_name, hookspec_name):
        plugin = plugin_manager._ensure_plugin(plugin_name)
        return any(
            impl.plugin_name == plugin_manager.get_name(plugin)
            for impl in getattr(plugin_manager.hook, hookspec_name).get_hookimpls()
        )

    plugin_manager.provides = _provides
    return plugin_manager


@pytest.fixture
def test_case():
    # each filename stem in `cases` will be run as an independent tox env
    case_name = os.getenv("TOX_ENV_NAME") or os.getenv("TEST_CASE")
    assert case_name

    CASE_DIR = Path(__file__).parent / "cases"
    case_file = next(f for f in CASE_DIR.glob("*.[y|ya]ml") if f.stem == case_name)
    assert case_file.exists()

    return TC.from_file(case_file)


def test_discovery(test_case, pm):
    for plugin in test_case.plugins:
        if plugin.name not in pm.plugins:
            er = "\n".join(str(e) for e in pm.get_errors(plugin.name))
            raise AssertionError(f"plugin name {plugin.name} was not registered:\n{er}")
        for hook in plugin.hooks:
            assert pm.provides(plugin.name, hook)


def test_dockwidget_added(test_case: TC, pm: NapariPluginManager, qtbot):
    for plugin in test_case.plugins:
        if plugin.name in pm._dock_widgets:
            for widget_name in pm._dock_widgets[plugin.name]:
                viewer = Viewer(show=False)
                try:
                    dw, wdg = viewer.window.add_plugin_dock_widget(
                        plugin.name, widget_name
                    )
                    assert isinstance(dw, QDockWidget)
                    print(dw)
                finally:
                    viewer.close()
