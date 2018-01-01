import logging
from celery_connectors.utils import get_percent_done
from celery_connectors.log.setup_logging import setup_logging
from tests.base_test import BaseTestCase

setup_logging()
log = logging.getLogger("test subprocess module")


class TestSubprocessModule(BaseTestCase):

    def test_subprocess_call(self):
        log.info("test_subprocess_call - start")
        test_file = "/tmp/nerfball-test-failed-subprocess_call-works"
        import subprocess

        # import pdb
        # pdb.set_trace() helpful to go in and debug

        # fail if this failed to delete a previous run
        assert(subprocess.call(["rm", "-f", test_file]) == 0)
        self.fail_if_test_file_exists(test_file=test_file)

        # fail if this failed and ran the nerfed module
        assert(subprocess.call(["touch", test_file]) == 0)
        self.fail_if_test_file_exists(test_file=test_file)

        log.info("test_subprocess_call - end")
    # end of test_subprocess_call

# end of TestSubprocessModule
