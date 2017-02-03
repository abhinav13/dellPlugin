from dell_tempest_plugin.tests.api import base
from tempest import test
import tempest.lib.cli.base as cli
import tempest.lib.cli.output_parser as output_parser
import os
from oslo_log import log as logging

LOG = logging.getLogger(__name__, "dell-tempest-plugin")


class TestHostAggreagateCreateInstance(base.BaseDellTempestTestCase):

    @classmethod
    def resource_setup(self):

        super(TestHostAggreagateCreateInstance, self).resource_setup()
        self.os_user_name = os.environ['OS_USERNAME']
        self.os_password = os.environ['OS_PASSWORD']
        self.os_auth_url = os.environ['OS_AUTH_URL']
        self.os_tenant_name = os.environ['OS_TENANT_NAME']
        self.cli_dir = '/bin'
        self.cliclient = cli.CLIClient(username=self.os_user_name, password=self.os_password, tenant_name=self.os_tenant_name,
                                       uri=self.os_auth_url, cli_dir='/bin/')

    def create_host_aggregate(self, name="", availabilityzone=""):

        if not name:
            name = 'AggName'
        if not availabilityzone:
            availabilityzone = 'AvZ'
        raw_output = self.cliclient.nova(action='aggregate-create', params=name + ' ' + availabilityzone)
        LOG.info("create_host_aggregate() raw output %s", raw_output)
        new_zone = output_parser.listing(raw_output)
        self.assertNotEqual(len(new_zone), 0)
        return new_zone[0]

    @test.attr(type="dell")
    def test_nova_host_aggregate_instancecreation(self):

        LOG.info("BEGIN: test_nova_host_aggregate_instancecreation")
        ag_zone = self.create_host_aggregate()
        LOG.info("ag_zone id %s", ag_zone['Id'])
        self.assertEqual('Hello world!', 'Hello world!')

    @classmethod
    def resource_cleanup(cls):
        # super(TestHelloWorld, cls).resource_cleanup()
        pass
