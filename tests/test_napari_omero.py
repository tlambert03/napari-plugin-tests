def test_discovery(pm):
    assert "omero" in pm.plugins
    assert "ome-types" in pm.plugins
    assert pm.provides('omero', 'napari_get_reader')
    assert pm.provides('omero', 'napari_experimental_provide_dock_widget')
    assert pm.provides('ome-types', 'napari_get_reader')
    assert pm.provides('ome-types', 'napari_experimental_provide_dock_widget')
