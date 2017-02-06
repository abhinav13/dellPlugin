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
            name = 'AggName' + str(self.getUniqueInteger())
        if not availabilityzone:
            availabilityzone = 'AvZ' + str(self.getUniqueInteger())
        raw_output = self.cliclient.nova(action='aggregate-create', params=name + ' ' + availabilityzone)
        LOG.info("create_host_aggregate() raw output %s", raw_output)
        new_zone = output_parser.listing(raw_output)
        self.assertNotEqual(len(new_zone), 0)
        return new_zone[0]

    def get_compute_host_details(self):
        raw_output = self.cliclient.nova(action='host-list')
        all_hosts = output_parser.listing(raw_output)
        LOG.info("get_compute_host_details raw output %s", raw_output)
        LOG.info("get_compute_host_details listing %s type %s", str(all_hosts),str(type(all_hosts)))

        self.assertNotEmpty(all_hosts)
        #Filter the host list for compute nodes only
        compute_hosts = list(filter(lambda x: str(x['service']).lower() == 'compute', all_hosts))
        LOG.info("compute_hosts %s", str(compute_hosts))
        self.assertNotEmpty(compute_hosts)
        return compute_hosts[0]

    def add_compute_host_to_aggregate_zone(self,agg_id,host_name):
        ret_val= self.cliclient.nova(action='aggregate-add-host', params=agg_id + ' ' + host_name)
        LOG.info("return value of adding host  %s", ret_val)

    @test.attr(type="dell")
    def test_nova_host_aggregate_instancecreation(self):
        LOG.info("BEGIN: test_nova_host_aggregate_instancecreation")
        ag_zone = self.create_host_aggregate()
        LOG.info("ag_zone id %s", ag_zone['Id'])
        host_details = self.get_compute_host_details()
        LOG.info("Host name where will create instances %s", str(host_details['host_name']))
        self.add_compute_host_to_aggregate_zone(ag_zone['Id'], host_details['host_name'])
        self.assertEqual('Hello world!', 'Hello world!')

    @classmethod
    def resource_cleanup(cls):
        # super(TestHelloWorld, cls).resource_cleanup()
        pass
