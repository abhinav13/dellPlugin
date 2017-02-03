from oslo_log import log as logging
from tempest import config
from tempest import test
import os
import tempest.lib.cli.base as cli

CONF = config.CONF
LOG = logging.getLogger(__name__)


class BaseDellTempestTest(test.BaseTestCase):

    @classmethod
    def skip_checks(self):
        pass

    def __init__(self):
        print "In Base init"
        self.os_user_name = os.environ['OS_USERNAME']
        self.os_password = os.environ['OS_PASSWORD']
        self.os_auth_url = os.environ['OS_AUTH_URL']
        self.os_tenant_name = os.environ['OS_TENANT_NAME']
        self.cli_dir = '/bin'
        self.cliclient = cli.CLIClient(username=self.os_user_name,password=self.os_password, tenant_name=self.os_tenant_name,
                                       uri=self.os_auth_url,cli_dir='/bin/')
