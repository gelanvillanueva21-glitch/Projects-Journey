from Config.config import settings
import hmac
import hashlib



def create_hmac(user_id : bytes):
    return hmac.new(
        settings.hmac_key.encode("utf-8"), 
        user_id, 
        hashlib.sha256).hexdigest()



def verify_hmac(user_id : bytes, hmac_signature : str) -> bool:
    return hmac.compare_digest(
        create_hmac(user_id),
        hmac_signature
    )




