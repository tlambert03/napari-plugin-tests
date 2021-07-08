def test_discovery(pm):
    assert "omero" in pm.plugins
    assert "omero-types" in pm.plugins
    assert pm.provides('omero', 'napari_get_reader')
    assert pm.provides('omero', 'napari_experimental_provide_dock_widget')
    assert pm.provides('omero-types', 'napari_get_reader')
    assert pm.provides('omero-types', 'napari_experimental_provide_dock_widget')
