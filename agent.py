from pydbus import SystemBus
import logging
logging.basicConfig(level=logging.DEBUG)


def trust_device(path):
  bus = SystemBus()
  logging.info('trust_device(path=%s)' % (path))
  dev = bus.get('org.bluez', path)['org.bluez.Device1']
  dev.Trusted = True

### Look into this one - not used, where did it come from?
def connect_device(path):
  bus = SystemBus()
  logging.info('connect_device(path=%s)' % (path))
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
      logging.info('Release()')

    def AuthorizeService(self, device, uuid):
      logging.info('Agent:AuthorizeService(device=%s, uuid=%s): automatic yes' % (device, uuid))
      return

    def RequestPinCode(self, device):
      logging.info('Agent:RequestPinCode(device=%s) -> 111111' % (device))
      trust_device(device)
      return 111111

    def RequestPasskey(self, device):
      """Callback for KeyboardOnly/xxx; returning a 6-digit passkey to the device"""
      trust_device(device)
      logging.info('Agent:RequestPasskey(device=%s) -> 111111' % (device))
      return 111111

    def DisplayPasskey(self, device, passkey, entered):
      logging.info('Agent:DisplayPasskey(device=%s, passkey=%s, entered=%s)' % (device, passkey, entered))
      print("DisplayPasskey (%s, %06u entered %u)" % (device, passkey, entered))

    def DisplayPinCode(self, device, pincode):
      logging.info('Agent:DisplayPinCode(device=%s, pincode=%s)' % (device, pindcode))
      print("DisplayPinCode (%s, %s)" % (device, pincode))

    def RequestConfirmation(self, device, passkey):
      """Callback for DisplayYesNo/DisplayOnly/KeyboardDisplay; device sent a 6-digit passkey, and we just confirm"""
      logging.info('Agent:RequestConfirmation(device=%s, passkey=%s)' % (device, passkey))
      trust_device(device)
      return

    def RequestAuthorization(self, device):
      logging.info('Agent:RequestAuthorization(device=%s)' % (device, passkey))
      print("RequestAuthorization (%s)" % (device))
      authorize = input("Authorize? (yes/no): ")
      return

    def Cancel(self):
      logging.info('Agent:Cancel()')
