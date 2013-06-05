import unittest
import beanstalkc
import logging

log = logging.getLogger(__name__)

class TestBeanstalkc(unittest.TestCase):
    def setUp(self):
        self.beanstalk = beanstalkc.Connection(host='localhost', port=11300)
        # flush queue
        while True :
            job = self.beanstalk.reserve(timeout=2)
            if job :
                log.debug("Flushing job with body {}".format(job.body))
                job.delete()
            else :
                break
        
    
    def tearDown(self):
        self.beanstalk.close()
         
    def test_stats(self):
        print(self.beanstalk.stats())
        
    def test_submit_receive(self):
        data = "hello world!"
        self.beanstalk.put(data)
        job = self.beanstalk.reserve()
        self.assertEqual(data.encode(), job.body)
