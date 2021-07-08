# automated CI for testing napari plugins

[![Status](https://github.com/tlambert03/napari-plugin-tests/actions/workflows/test.yml/badge.svg)](https://github.com/tlambert03/napari-plugin-tests/actions/workflows/test.yml)

## How this works

To add a test case for a plugin, open a PR to add a new file
to the [`cases`](cases) directory.  Here's an example test case, for
`napari-omero`, which has a somewhat complicated installation,
involving conda dependencies and non-default channels.

```yaml
# cases/napari-omero.yml
deps: napari-omero  # pip dependencies
conda_channels: ome  # conda channels to use
conda_deps: omero-py  # deps to install from conda
plugins:
  - name: omero  # plugin names that should be found
    hooks:  # hooks that this plugin should have registered
      - napari_get_reader
      - napari_experimental_provide_dock_widget
```

This will extend the [`tox.ini`](tox.ini) in this directory with
a test-case specific testenv:

```ini
[testenv:napari-omero]
conda_deps =
  omero-py
conda_channels =
  ome
deps =
  {[testenv]deps}
  napari-omero
```

and, using that environment, will run the tests in
[`test_cases`](test_cases.py). Currently the default test will just ensure
that the pacakge is discovered correctly, and that the expected
hooks have been registered for each plugin namespace provided by
the package, but this can expand with the TestCase schema.
