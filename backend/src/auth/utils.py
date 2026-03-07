from passlib.context import CryptContext
from datetime import timedelta, datetime,timezone
from src.config import Config
import jwt
import uuid, os
import logging
from itsdangerous import URLSafeTimedSerializer

# In-memory Token Blacklist
TOKEN_BLACKLIST = set()

passwd_context = CryptContext (
    schemes=['pbkdf2_sha256']
)

def generate_passwd_hash(password: str) -> str:
    hash = passwd_context.hash(password)
    return hash

def verify_password(password: str, hash:str) -> bool:
    return passwd_context.verify(password,hash)

def create_access_token(
    userdata: dict,
    expiry: timedelta | None = None,
    refresh: bool = False,
):
    now = datetime.now(timezone.utc)

    payload = {
        "user": userdata,
        "exp": now + (expiry or timedelta(seconds=Config.ACCESS_TOKEN_EXPIRY)),
        "iat": now,
        "jti": str(uuid.uuid4()),
        "refresh": refresh,
    }

    return jwt.encode(
        payload,
        Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM,
    )

def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=Config.JWT_ALGORITHM
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None

def revoke_token(token: str):
    TOKEN_BLACKLIST.add(token)
    
serializer = URLSafeTimedSerializer(
    secret_key=Config.JWT_SECRET, salt="email-configuration"
)

def create_url_safe_token(data: dict):
    token = serializer.dumps(data)
    return token

def decode_url_safe_token(token:str):
    try:
        token_data = serializer.loads(token)
        return token_data
    except Exception as e:
        logging.error(str(e))
        
def generate_unique_filename(original_filename: str) -> str:
    ext = os.path.splitext(original_filename)[1] 
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"user_{timestamp}{ext}"
    return filename