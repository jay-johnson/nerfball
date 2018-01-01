import logging
from celery_connectors.utils import get_percent_done
from celery_connectors.log.setup_logging import setup_logging
from tests.base_test import BaseTestCase

setup_logging()
log = logging.getLogger("test imp module")


class TestImpModule(BaseTestCase):

    def test_imp_load_source(self):
        log.info("test_imp_load_source - start")
        test_file = "/tmp/nerfball-test-failed-imp_load_source-works"
        import imp

        # import pdb
        # pdb.set_trace() helpful to go in and debug

        # fail if this failed to delete a previous run
        try:
            assert(not imp.load_source(name="imp", pathname="./nerfball/imp.py"))
        except Exception as e:
            assert(str(e) == "IMP_LOAD_SOURCE - NERFED")

        log.info("test_imp_load_source - end")
    # end of test_imp_load_source

# end of TestImpModule
