import logging
from celery_connectors.utils import get_percent_done
from celery_connectors.log.setup_logging import setup_logging
from tests.base_test import BaseTestCase

setup_logging()
log = logging.getLogger("test os module")


class TestOSModule(BaseTestCase):

    def test_os_system(self):
        log.info("test_os_system - start")
        test_file = "/tmp/nerfball-test-failed-os-system-works"
        import os

        # import pdb
        # pdb.set_trace() helpful to go in and debug

        os.system(("rm -f {}; touch {}")
                  .format(test_file,
                          test_file))

        self.fail_if_test_file_exists(test_file=test_file)

        log.info("test_os_system - end")
    # end of test_os_system

# end of TestOSModule
