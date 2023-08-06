import ssl
# from nostr import Event
import time
from nostr.relay_manager import RelayManager
from nostr.key import PrivateKey
from nostr.event import Event
# from python_nostr import Event
# from python_nostr import RelayManager
# from python_nostr import PrivateKey
# from nostr.event import Event
# from nostr.relay_manager import RelayManager
# from nostr.key import PrivateKey
# import random
import os

# private_key = PrivateKey()
# print(private_key.bech32())
# public_key = private_key.public_key
# print("https://snort.social/p/"+private_key.public_key.bech32())
# print(private_key.public_key.bech32())

tags = []

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def post_note(private_key, content, tags=""):
    relay_manager = RelayManager()
    with open(__location__+'/relay_list.txt', 'r') as f:
        for line in f:
            relay_manager.add_relay(line.strip())
    # relay_manager.add_relay("wss://relay.nostr.bg")
    relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
    time.sleep(1.25) # allow the connections to open

    event = Event(private_key.public_key.hex(), content)
    print(f"event public key is {event.public_key}")
    # print(f"\n>> Event on snort.social: https://snort.social/e/{PublicKey.hex_to_bech32(event.id, 'Encoding.BECH32')}")

    # print(event.content)
    private_key.sign_event(event)

    relay_manager.publish_event(event)
    # event_public_key = PublicKey.hex_to_bech32(event.id, 'Encoding.BECH32')
    # print(event_public_key)
    print("note sent")
    time.sleep(1)

    relay_manager.close_connections()


# nostr_create_key_and_post(private_key, "#stackjoin", tags=["t","Stackjoin"])
# post_note(private_key, content="content todo", tags=[['t','stackjoin']])