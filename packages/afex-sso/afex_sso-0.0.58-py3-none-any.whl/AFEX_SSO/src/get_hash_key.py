import hashlib


def get_hash_key(api_key, secret_key, idempotency_key):
    try:
        de_hash = api_key + secret_key + idempotency_key
    except:
        de_hash = None

    hashed = hashlib.sha256(de_hash.encode('utf8')).hexdigest()

    return hashed
