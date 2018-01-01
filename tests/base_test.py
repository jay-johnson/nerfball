import os
import logging
import unittest

log = logging.getLogger("base_test")


class BaseTestCase(unittest.TestCase):

    debug = False

    def setUp(self):

        # most: python setup.py test will need
        # some of these for handling test cases
        os.environ["NERF_OS_POPEN"] = "0"
        os.environ["NERF_OS_REMOVE"] = "0"
        os.environ["NERF_SUBPROCESS_CALL"] = "0"

        if self.debug:
            print("setUp")

    # end of setUp

    def tearDown(self):
        if self.debug:
            print("tearDown")
    # end of tearDown

    def fail_if_test_file_exists(self,
                                 test_file=None):

        if os.path.exists(test_file):
            log.error("")
            log.error("Test failed with file={}".format(test_file))
            log.error("Please confirm nerf-virtualenv.sh has ran")
            log.error("")

        assert(not os.path.exists(test_file))
    # end of fail_if_test_file_exists

# end of BaseTestCase
