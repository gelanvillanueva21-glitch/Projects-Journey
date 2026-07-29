from Config.config import settings
import hmac
import hashlib



def create_hmac(user_id : bytes):
    return hmac.new(
        settings.hmac_key.encode("utf-8"), 
        user_id, 
        hashlib.sha256).hexdigest()



def verify_hmac(user_id : str, hmac_signature : str) -> bool:
    byte_id = user_id.encode("utf-8")
    new_signature = create_hmac(byte_id)
    return hmac.compare_digest(
        new_signature,
        hmac_signature
    )




