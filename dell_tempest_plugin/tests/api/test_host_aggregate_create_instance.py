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
        self.ag_zone = ''
        self.ag_zone_Id = None
        self.ag_zone_name = None
        self.host_name = None
        self.network_id = None
        self.boot_image_name = ''

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
        LOG.info("get_compute_host_details listing %s type %s", str(all_hosts), str(type(all_hosts)))

        self.assertNotEmpty(all_hosts)
        # Filter the host list for compute nodes only
        compute_hosts = list(filter(lambda x: str(x['service']).lower() == 'compute', all_hosts))
        LOG.info("compute_hosts %s", str(compute_hosts))
        self.assertNotEmpty(compute_hosts)
        return compute_hosts[0]

    def get_network_id(self, name="public"):
        raw_output = self.cliclient.openstack(action='network list')
        all_networks = output_parser.listing(raw_output)
        public_net = list(filter(lambda x: str(x['Name']).lower() == name, all_networks))
        self.assertNotEmpty(public_net)
        return public_net[0]['ID']

    def get_boot_image_name(self, name="cirros-0.3.4-x86_64-disk.img"):
        raw_output = self.cliclient.openstack(action='image list')
        all_images = output_parser.listing(raw_output)
        boot_img = list(filter(lambda x: str(x['Name']).lower() == name, all_images))
        self.assertNotEmpty(boot_img)
        return boot_img[0]['Name']

    def add_compute_host_to_aggregate_zone(self, agg_id, host_name):
        ret_val = self.cliclient.nova(action='aggregate-add-host', params=agg_id + ' ' + host_name)
        self.assertIn("successfully", ret_val)

    def remove_compute_host_from_aggregate_zone(self, agg_id, host_name):
        ret_val = self.cliclient.nova(action='aggregate-remove-host', params=agg_id + ' ' + host_name)
        self.assertIn("successfully", ret_val)

    def delete_host_aggregate(self):
        ret_val = self.cliclient.nova(action='aggregate-delete', params=self.ag_zone['Id'])
        self.assertIn("successfully", ret_val)

    def boot_image_on_aggregate_zone(self):
        raw_output = self.cliclient.nova(action='boot', params='--flavor 1'+ ' --image=' + self.boot_image_name +
                                         ' --nic net-id='+self.network_id + ' --availability-zone=' +
                                         self.ag_zone_name + ' ' + self.getUniqueString('TestInstaci1e'))
        instance_info = output_parser.listing(raw_output)
        LOG.info("Output of boot image %s", instance_info)
        self.assertNotEmpty(instance_info)
        return instance_info[0]['Id']


    @test.attr(type="dell")
    def test_nova_host_aggregate_instancecreation(self):
        LOG.info("BEGIN: test_nova_host_aggregate_instancecreation")
        self.ag_zone = self.create_host_aggregate()
        self.ag_zone_Id = self.ag_zone['Id']
        self.ag_zone_name = self.ag_zone['Availability Zone']
        LOG.info("ag_zone id %s", self.ag_zone_Id)
        self.host_details = self.get_compute_host_details()
        LOG.info("Host name where will create instances %s", str(self.host_details['host_name']))
        self.add_compute_host_to_aggregate_zone(self.ag_zone_Id, self.host_details['host_name'])

        # Now get network image
        self.network_id = self.get_network_id()
        self.boot_image_name = self.get_boot_image_name()
        instance_id = self.boot_image_on_aggregate_zone()
        LOG.info("Booted this image now %s", str(instance_id))
        self.assertEqual('Hello world!', 'Hello world!')

        # Clean up stuff that you created
        #self.remove_compute_host_from_aggregate_zone(self.ag_zone['Id'], self.host_details['host_name'])
        #self.delete_host_aggregate()

    @classmethod
    def resource_cleanup(cls):
        # super(TestHelloWorld, cls).resource_cleanup()
        pass
