import hmac, hashlib
from hmac import compare_digest

from config import WEBHOOK_SECRET

# FUNCTION THAT VERIFIES THE REQUEST WAS SENT BY GITHUB OR NOT

def verify_request(headers, body):
    # RETRIEVING THE GITHUB SIGNATURE HEADER
    signature_header = headers.get('x-hub-signature-256')

    # ENCODE THE SECRET INTO BYTES
    secret = WEBHOOK_SECRET
    secret_bytes = secret.encode('utf-8')

    computated_signature = "sha256=" + hmac.new(
        key=secret_bytes,
        msg=body,
        digestmod=hashlib.sha256
    ).hexdigest()

    return compare_digest(computated_signature, signature_header)