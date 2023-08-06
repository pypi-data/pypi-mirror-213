import warnings

from diveplane.utilities.installation_verification import InstallationCheckRegistry
from diveplane.utilities.installation_verification import configure


def test_installation():
    print("[bold]Validating Diveplane:registered: Installation")
    registry = InstallationCheckRegistry()
    configure(registry)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")