import base
import tempest.lib.cli.parser as parser
class myTest(base.BaseDellTempestTest):
    def __init__(self):
        print  "in derived init"
        super(myTest, self).__init__()

    @classmethod
    def resource_setup(cls):
        super(myTest,cls).resource_setup()

    @classmethod
    def resource_cleanup(cls):
        super(myTest,cls).resource_cleanup()

    def testthis(self):
        print "Now Printing stuff"
        print self.os_user_name
        print self.os_auth_url


d = myTest()
d.testthis()
parser.details("Output")
