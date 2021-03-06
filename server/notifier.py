import os
from apns import APNs, Payload

test_token = "8d5a5b8232248d2d820d6324c6865adbbfe118ae866b3e6680177e43fe9dbb34"
# old_cert_path = ./production_im.subl.reactjs.native.SimpleChat.pem"

CERT_PATH = os.environ["CERT_PATH"]

apn_service = APNs(use_sandbox=True, cert_file=CERT_PATH)

print "cert_path: {}, apns connected: {}".format(CERT_PATH, apn_service.gateway_server.connection_alive)


def send_message(token, message):
    print "Sending {} to {}".format(message["text"], token)
    p = Payload(alert="{user[name]}: {text}".format(**message),
                sound="default",
                badge=1)
    apn_service.gateway_server.send_notification(token, p)
    print "Done Sending {} to {}".format(message["text"], token)
