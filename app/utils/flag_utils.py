import hashlib
import base64
import re
import logging
from app.config import Config

logger = logging.getLogger(__name__)

def hash_flag(flag):
    """Create MD5 hash of a flag string"""
    return hashlib.md5(flag.encode()).hexdigest()

def validate_flag(flag_id, flag_value):
    """Validate the submitted flag against stored hash"""
    if flag_id not in Config.FLAG_HASHES:
        logger.warning(f"Attempted validation with invalid flag_id: {flag_id}")
        return False
    
    expected_hash = Config.FLAG_HASHES.get(flag_id)
    submitted_hash = hash_flag(flag_value)
    
    result = submitted_hash == expected_hash
    if result:
        logger.info(f"Flag {flag_id} successfully validated")
    else:
        logger.warning(f"Flag {flag_id} validation failed")
        
    return result

def encode_base64(text):
    """Encode text to base64"""
    return base64.b64encode(text.encode()).decode()

def decode_base64(encoded_text):
    """Decode base64 text"""
    try:
        return base64.b64decode(encoded_text).decode()
    except:
        return None

def caesar_cipher(text, shift=3):
    """Apply Caesar cipher to text"""
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord('a') if char.islower() else ord('A')
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    return result

def url_encode(text):
    """URL encode text without using external libraries"""
    import urllib.parse
    return urllib.parse.quote(text)

def url_decode(text):
    """URL decode text without using external libraries"""
    import urllib.parse
    return urllib.parse.unquote(text)

def obfuscate_html(text):
    """Simple HTML obfuscation technique"""
    # Convert to HTML entities
    result = ""
    for char in text:
        result += f"&#{ord(char)};"
    return result

def detect_xss(user_input):
    """Basic XSS detection"""
    xss_patterns = [
        r'<script.*?>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',
        r'<img.*?onerror=',
        r'alert\s*\('
    ]
    
    for pattern in xss_patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            return True
    
    return False