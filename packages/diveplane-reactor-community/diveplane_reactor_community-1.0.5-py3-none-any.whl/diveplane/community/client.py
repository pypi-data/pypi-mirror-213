from concurrent.futures import ThreadPoolExecutor, Future
from contextlib import contextmanager
import json
import logging
from typing import Union
from packaging.version import parse as parse_version

import certifi
from diveplane.direct import DiveplaneDirectClient
from diveplane.community import __version__ as community_version
import urllib3
from urllib3.util import Retry, Timeout


logger = logging.getLogger(__name__)
# If True, the version has already been checked for this process.
VERSION_HOST = "https://version-check.diveplane.com"
_VERSION_CHECKED = False


@contextmanager
def squelch_logs(log_level: int):
    """A context manager to temporarily disable logs."""
    _old_level = logging.root.manager.disable
    logging.disable(log_level)
    try:
        yield
    finally:
        logging.disable(_old_level)


class DiveplaneCommunityClient(DiveplaneDirectClient):

    """
    Creates a distinct DiveplaneDirectClient for diveplane-reactor-community.

    Parameters
    ----------
    verbose : bool, default False
        Set verbose output.
    debug: bool, default False
        Sets logger debug output.
    """

    def __init__(self, verbose=False, debug=False, **kwargs):
        """
        Creates a DiveplaneClient which executes via a direct interface using dynamic libraries.

        Parameters
        ----------
        verbose : bool, default False
            Set verbose output.
        debug: bool, default False
            Sets logger debug output.
        """
        global _VERSION_CHECKED
        with ThreadPoolExecutor(max_workers=1) as executor:
            if kwargs.pop("check_version", True) and not _VERSION_CHECKED:
                _VERSION_CHECKED = True
                self.version_check_task = executor.submit(self.check_version)
                self.version_check_task.add_done_callback(self.report_version)
        super().__init__(verbose=verbose, debug=debug, **kwargs)

    def check_version(self) -> Union[str, None]:
        """Check if there is a more recent version."""
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                                   ca_certs=certifi.where(),
                                   retries=Retry(total=1),
                                   timeout=Timeout(total=3),
                                   maxsize=10)
        url = f"{VERSION_HOST}/v1/diveplane-reactor-community?version={community_version}"
        with squelch_logs(logging.WARNING + 1):
            response = http.request(method="GET", url=url)
        if 200 <= response.status < 300:
            payload = json.loads(response.data.decode('utf-8'))
            return payload.get('version')
        raise AssertionError("Not OK response.")

    def report_version(self, task: Future):
        try:
            latest_version = task.result()
        except Exception:
            pass
        else:
            if latest_version and latest_version != community_version:
                if parse_version(latest_version) > parse_version(community_version):
                    logger.warning(
                        f"Version {latest_version} of Diveplane® Reactor Community is "
                        f"available. You are using version {community_version}.")
                elif parse_version(latest_version) < parse_version(community_version):
                    logger.debug(
                        f"Version {latest_version} of Diveplane® Reactor Community is "
                        f"available. You are using version {community_version}. "
                        f"This is a pre-release version.")
