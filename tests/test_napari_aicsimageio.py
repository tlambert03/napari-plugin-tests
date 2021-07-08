def test_discovery(pm):
    assert "aicsimageio-in-memory" in pm.plugins
    assert "aicsimageio-out-of-memory" in pm.plugins
    assert pm.provides('aicsimageio-in-memory', 'napari_get_reader')
    assert pm.provides('aicsimageio-out-of-memory', 'napari_get_reader')
