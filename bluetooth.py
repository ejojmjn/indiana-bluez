from gi.repository import GLib
from pydbus import SystemBus

from agent import Agent

import sys
import logging
logging.basicConfig(level=logging.DEBUG)

AGENT_PATH = "/star/wars"

def all_adapters():
  bus = SystemBus()
  bluez = bus.get("org.bluez", "/")
  adapters = { k: v['org.bluez.Adapter1'] for k, v in bluez.GetManagedObjects().items() if 'org.bluez.Adapter1' in v}
  logging.info('all_adapters() -> %s' % list(adapters.keys()))
  return adapters

def configure_adapter(path):
  bus = SystemBus()
  adapter = bus.get('org.bluez', path)
  # ofono crashes when hfp is negotiated if Powered=True. Mystery...
  #adapter.Powered = True
  adapter.Discoverable = True
  adapter.PairableTimeout = 0
  adapter.DiscoverableTimeout = 0
  logging.info('configure_adapter(path=%s) Powered=True Discoverable=True' % (path))

def register_agent(capability):
  bus = SystemBus()
  manager = bus.get('org.bluez')['.AgentManager1']
  manager.RegisterAgent(AGENT_PATH, capability)
  logging.info('register_agent:manager.RegisterAgent(path=%s, capability=%s)' % (AGENT_PATH, capability))
  manager.RequestDefaultAgent(AGENT_PATH)
  logging.info('register_agent:manager.RequestDefaultAgent(path=%s)' % (AGENT_PATH))
  bus.register_object(AGENT_PATH, Agent(), node_info=None)
  logging.info('register_agent:bus.register_object(path=%s)' % (AGENT_PATH))

def unregister_agent():
  bus = SystemBus()
  manager = bus.get('org.bluez')['.AgentManager1']
  manager.UnregisterAgent(AGENT_PATH)
  logging.info('register_agent:UnregisterAgent(path=%s)' % (AGENT_PATH))


# Adapter => a Bluetooth adapter
# Device  => e.g. a phone connecting via Bluetooth
# Agent   => a handler (object) for authentication of connections attempts to an adapter

if __name__ == '__main__':

  adapters = [configure_adapter(a) for a in all_adapters().keys()]

#  if len(adapters) == 0:
#    sys.exit("No Bluetooth adapters found; exiting!")

  capability = "DisplayYesNo" # DisplayOnly DisplayYesNo
                              # KeyboardOnly KeyboardDisplay
  register_agent(capability)

  try:
    mainloop = GLib.MainLoop()
    mainloop.run()
  except (KeyboardInterrupt):
    unregister_agent()
    mainloop.quit()
    print("\nStopped with Control-C")
