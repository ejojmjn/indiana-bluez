from gi.repository import GLib
from pydbus import SystemBus

import logging
logging.basicConfig(level=logging.DEBUG)


def ask(prompt):
  return 111111

def set_trusted(path):
    props = bus.get('org.bluez', path)['org.freedesktop.DBus.Properties']
    print('trust', path)
    props.Set("org.bluez.Device1", "Trusted", GLib.Variant.new_boolean(True))

def dev_connect(path):
    dev = bus.get('org.bluez', path)['org.bluez.Device1']
    dev.Connect()

class Agent(object):
    '''
<node>
	<interface name='org.bluez.Agent1'>
		<method name='Release'></method>
		<method name='AuthorizeService'>
			<arg type='o' name='device' direction='in'/>
			<arg type='s' name='uuid' direction='in'/>
		</method>
		<method name='RequestPinCode'>
			<arg type='o' name='device' direction='in'/>
			<arg type='s' name='pin_code' direction='out'/>
		</method>
		<method name='RequestPasskey'>
			<arg type='o' name='device' direction='in'/>
			<arg type='u' name='pass_key' direction='out'/>
		</method>
		<method name='DisplayPasskey'>
			<arg type='o' name='device' direction='in'/>
			<arg type='u' name='pass_key' direction='in'/>
			<arg type='q' name='entered' direction='in'/>
		</method>
		<method name='DisplayPinCode'>
			<arg type='o' name='device' direction='in'/>
			<arg type='s' name='pin_code' direction='in'/>
		</method>
		<method name='RequestConfirmation'>
			<arg type='o' name='device' direction='in'/>
			<arg type='u' name='pass_key' direction='in'/>
		</method>
		<method name='RequestAuthorization'>
			<arg type='o' name='device' direction='in'/>
		</method>
        <method name='Cancel'></method>
	</interface>
</node>
    '''
    def Release(self):
        print("Release")

    def AuthorizeService(self, device, uuid):
        print("AuthorizeService (%s, %s)" % (device, uuid))
        authorize = ask("Authorize connection (yes/no): ")
        if (authorize == "yes"):
            return

    def RequestPinCode(self, device):
        print("RequestPinCode (%s)" % (device))
        set_trusted(device)
        return ask("Enter PIN Code: ")

    def RequestPasskey(self, device):
        print("RequestPasskey (%s)" % (device))
        set_trusted(device)
        passkey = ask("Enter passkey: ")
        return int(passkey)

    def DisplayPasskey(self, device, passkey, entered):
        print("DisplayPasskey (%s, %06u entered %u)" %
              (device, passkey, entered))

    def DisplayPinCode(self, device, pincode):
        print("DisplayPinCode (%s, %s)" % (device, pincode))

    def RequestConfirmation(self, device, passkey):
        print("RequestConfirmation (%s, %06d)" % (device, passkey))
        set_trusted(device)
        print("here")
        return True
#        confirm = ask("Confirm passkey ([y]/n): ")

    def RequestAuthorization(self, device):
        print("RequestAuthorization (%s)" % (device))
        auth = ask("Authorize? ([y]/n): ")

    def Cancel(self):
        print("Cancel")

def all_adapters():
  bus = SystemBus()
  bluez = bus.get("org.bluez", "/")
  adapters = { k: v['org.bluez.Adapter1'] for k, v in bluez.GetManagedObjects().items() if 'org.bluez.Adapter1' in v}
  logging.info('all_adapters() -> %s' % list(adapters.keys()))
  return adapters

def configure_adapter(obj_path):
    props = bus.get('org.bluez', obj_path)['org.freedesktop.DBus.Properties']
    props.Set("org.bluez.Adapter1", "Powered", GLib.Variant.new_boolean(True))
    props.Set("org.bluez.Adapter1", "Discoverable", GLib.Variant.new_boolean(True))
    logging.info('configure_adapter(obj_path=%s) Powered=True Discoverable=True' % (obj_path))

def register_agent():
    capability = "DisplayYesNo"
    path = "/net/lvht/btk/agent"
    # agent = Agent(bus.con, path)
    bus.register_object(path, Agent(), node_info=None)
    manager = bus.get('org.bluez')['.AgentManager1']
    manager.RegisterAgent(path, capability)
    manager.RequestDefaultAgent(path)



if __name__ == '__main__':

    bus = SystemBus()

    [configure_adapter(a) for a in all_adapters().keys()]

    register_agent()

    mainloop = GLib.MainLoop()

    mainloop.run()
