"""
Project: META-SHARE
Utility functions for unit tests useful across apps.
"""
import os
from metashare import settings
from xml.etree.ElementTree import fromstring
from metashare.repo2.models import resourceInfoType_model
from django.test.testcases import TestCase
from django.core.management import call_command

def setup_test_storage():
    settings.STORAGE_PATH = '{0}/test-tmp'.format(settings.ROOT_PATH)
    try:
        os.mkdir(settings.STORAGE_PATH)
    except:
        pass

def import_xml(filename):
    _xml = open(filename)
    _xml_string = _xml.read()
    _xml.close()
    _tree = fromstring(_xml_string)
    
    result = resourceInfoType_model.import_from_elementtree(_tree)
    return result


class IndexAwareTestCase(TestCase):
    """
    A Django `TestCase` which makes sure to always rebuild the search index
    before and after every test so that it always matches the current database
    state.
    """
    def _fixture_setup(self):
        result = super(IndexAwareTestCase, self)._fixture_setup()
        call_command('rebuild_index', interactive=False,
                     using=settings.TEST_MODE_NAME)
        return result

    def _fixture_teardown(self):
        result = super(IndexAwareTestCase, self)._fixture_teardown()
        call_command('rebuild_index', interactive=False,
                     using=settings.TEST_MODE_NAME)
        return result
