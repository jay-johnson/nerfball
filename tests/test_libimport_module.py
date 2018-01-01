import logging
from celery_connectors.utils import get_percent_done
from celery_connectors.log.setup_logging import setup_logging
from tests.base_test import BaseTestCase

setup_logging()
log = logging.getLogger("test libimport module")


class TestLibImportModule(BaseTestCase):

    def test_importlib_machinery_sourcefileloader(self):
        log.info("test_importlib_machinery_sourcefileloader - start")
        test_file = "/tmp/nerfball-test-failed-libimport_load_source-works"
        import types
        import importlib.machinery

        # import pdb
        # pdb.set_trace() helpful to go in and debug

        # fail if this failed to delete a previous run
        try:
            loader = importlib.machinery.SourceFileLoader("imp", "./nerfball/imp.py")
            mod = types.ModuleType(loader.name)
            loader.exec_module(mod)
            print(mod)
            assert(not mod)
        except Exception as e:
            assert(str(e) == "SourceFileLoader - NERFED")

        log.info("test_importlib_machinery_sourcefileloader - end")
    # end of test_importlib_machinery_sourcefileloader

# end of TestLibImportModule
