import os
import unittest2
from google.appengine.api import memcache
from google.appengine.ext import testbed
from google.appengine.ext.testbed import DATASTORE_SERVICE_NAME
from google.appengine.datastore import datastore_stub_util
import logging
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import urlfetch_stub

from google.appengine.api import datastore_file_stub
import main
import webapp2
import pickle
import base64


class BasicTestCase(unittest2.TestCase):

    def setUP(self):
        """ Override this method
        """
        pass

    @classmethod
    def setUpClass(cls):
        cls.set_up_testbed()

    @classmethod
    def set_up_testbed(cls):
        """ Slowly building up set_up_testbed

            apiproxy_stup_map settings first
        """
        apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
        apiproxy_stub_map.apiproxy.RegisterStub('urlfetch', urlfetch_stub.URLFetchServiceStub())

        # First, create an instance of the Testbed class.
        cls.testbed = testbed.Testbed()

        cls.testbed.activate()

        cls.testbed.init_datastore_v3_stub()
        cls.testbed.init_memcache_stub()
        cls.testbed.init_taskqueue_stub(root_path=os.path.join(os.path.dirname(__file__), '../..'))
        cls.taskqueue_stub = apiproxy_stub_map.apiproxy.GetStub('taskqueue')
        cls.testbed.init_memcache_stub()

        # Set request variables, so that i18n does not break
        cls.app = main.app
        cls.app.set_globals(app=cls.app, request=webapp2.Request.blank('/'))

    @classmethod
    def run_taskqueue(cls):
        """ Have not been able to get taskqueues to work yet
        
            http://stackoverflow.com/questions/6632809/gae-unit-testing-taskqueue-with-testbed
        """
        return
        taskq = cls.testbed.get_stub(testbed.TASKQUEUE_SERVICE_NAME)
        for q in taskq.GetQueues():
            logging.warning("running tasks for %s" % q["name"])
            tasks = taskq.GetTasks(q["name"])
            taskq.FlushQueue(q["name"])
            while tasks:
                for task in tasks:
                    logging.warning("executing: %s" % task["url"])
                    params = base64.b64decode(task["body"])
                    logging.warning(params)
                    if task['url']:
                        # normal taskque as post executed here
                        response = cls.app.post(task["url"], params)
                    else:
                        # when defer.deferred is called with a function it needs to be done like this
                        try:
                            (func, args, opts) = pickle.loads(base64.b64decode(task["body"]))
                            func(*args)
                        except Exception, e:
                            logging.exception(e)
                            logging.warning(task)
                tasks = taskq.GetTasks(q["name"])
                taskq.FlushQueue(q["name"])
        for q in taskq.GetQueues():
            if q["tasks_in_queue"]:
                logging.warning("can't run for: %s" % q["name"])

        return True

#     def test_0(self):
#         self.core_test()
#         pass

    def core_test(self):
        """ Some defaults simple test to see if test base is functional
        """
        self.datastore_test()
        self.memcache_test()
    
    def datastore_test(self):
        from practice.model.garage import Garage
        props = {"name": "test",
                 "postal_country": "NL",
                 "brand": "Lamborghini"}

        Garage.add(props=props)
        o = Garage.query().filter(Garage.name == props["name"]).get()
        if o:
            o.key.delete()
            if Garage.query().filter(Garage.name == props["name"]).get() is None:
                self.log("Datastore test OK!")

    def memcache_test(self):
        memcache.set("test", {"a": "Testing",
                              "b": "the",
                              "c": "memcache",
                              "d": "successful"})
        test = memcache.get("test")
        memcache.delete("test")
        if "%s %s %s %s!" % (test["a"], test["b"], test["c"], test["d"]) == "Testing the memcache successful!":
            self.log("Memcache test OK!")

    @classmethod
    def load_datastore(cls, datastore_image=None):
        """ Loads a datastore with test data
        
            NOT USED
        """
        cls.log("Loading datastore image: %s" % datastore_image)
        if not datastore_image:
            datastore_file = '/dev/null'
        else:
            datastore_file = os.path.join(os.path.dirname(__file__), '../testdata/' + datastore_image)

        cls.testbed.init_datastore_v3_stub(enable=False)
        cls.testbed.init_datastore_v3_stub(datastore_file=datastore_file, save_changes=False)

    @classmethod
    def tearDownClass(cls):
        cls.testbed.deactivate()
        
    """ Extra functions
    """
    @classmethod
    def log(cls, message):
        print message
