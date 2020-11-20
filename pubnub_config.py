from pubnub import pubnub
import pubnub_keys

def config(uuid):
  pnconfig = pubnub.PNConfiguration()
  pnconfig.subscribe_key=pubnub_keys.sub_key
  pnconfig.publish_key=pubnub_keys.pub_key
  pnconfig.uuid=uuid
  return pubnub.PubNub(pnconfig)
