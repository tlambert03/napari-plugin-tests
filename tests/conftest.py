import pytest


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
