from hello_world_tempest_plugin.tests.api import base
from tempest import test


class TestMyHello(base.BaseHelloWorldTest):

    @classmethod
    def resource_setup(cls):
        super(TestMyHello, cls).resource_setup()

    @test.attr(type="smoke")
    def test_nova_aggreagate_zone_instance_creation(self):
        self.assertNotEqual('Hello world!', 'Hello world!')

    @classmethod
    def resource_cleanup(cls):
        super(TestMyHello, cls).resource_cleanup()
