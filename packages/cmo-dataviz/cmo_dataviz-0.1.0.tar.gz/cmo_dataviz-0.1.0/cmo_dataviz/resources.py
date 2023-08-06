# Resources lookup file for dots_dataviz
import pathlib
from pkg_resources import resource_filename
import cmo_dataviz as cdv


# tutorial notebooks
_NOTEBOOK = {
    _.name: _
    for _ in pathlib.Path(resource_filename(cdv.__name__, "notebooks")).glob("*.ipynb")
}

# resource types
_RESOURCES = dict(notebook=_NOTEBOOK)


def _resource(resource_type, name: str) -> str:
    """Return the full path filename of a resource.
    :param str resource_type: The type of the resource.
    :param str  name: The name of the resource.
    :returns: The full path filename of the fixture data set.
    :rtype: str
    :raises FileNotFoundError: If the resource cannot be found.
    """
    full_path = _RESOURCES[resource_type].get(name, None)

    if full_path and full_path.exists():
        return str(full_path)

    raise FileNotFoundError(
        'Could not find {resource_type} "{name!s}"! Does it exist?'.format(
            resource_type=resource_type, name=name
        )
    )

def get_notebook_path(name: str) -> str:
    """Return the full path filename of a tutorial notebook.
    :param str name: The name of the notebook.
    :returns: The full path filename of the notebook.
    :rtype: str
    :raises FileNotFoundError: If the notebook cannot be found.
    """
    return _resource("notebook", name)