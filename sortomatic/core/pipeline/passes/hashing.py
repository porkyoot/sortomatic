import threading
from functools import partial
from ....l8n import Strings
from ...config import settings

try:
    import xxhash
except ImportError:
    xxhash = None

try:
    import imagehash
    from PIL import Image
except ImportError:
    imagehash = None
    Image = None

try:
    import pyacoustid
except ImportError:
    pyacoustid = None

# These are now backed by settings, but localized here for brevity if needed
# though we'll use settings directly in the functions.

def compute_hashes(ctx: dict):
    """Computes standard and perceptual hashes with a safety timeout."""
    
    def _worker():
        fpath = ctx['path']
        file_size = ctx['size_bytes']
        
        # 1. Fast Hash (First 4KB + Last 4KB)
        if file_size > 0 and xxhash:
            try:
                with open(fpath, 'rb') as f:
                    first_chunk = f.read(settings.fast_hash_size)
                    last_chunk = b''
                    if file_size > settings.fast_hash_size:
                        f.seek(-min(settings.fast_hash_size, file_size - settings.fast_hash_size), 2)
                        last_chunk = f.read(settings.fast_hash_size)
                    
                    hasher = xxhash.xxh64()
                    hasher.update(first_chunk)
                    hasher.update(last_chunk)
                    ctx['fast_hash'] = hasher.hexdigest()
            except Exception:
                ctx['fast_hash'] = None
        
        # 2. Perceptual Hash (Only for images)
        if ctx.get('category') == Strings.CAT_IMAGES and imagehash:
            try:
                with Image.open(fpath) as img:
                    ctx['perceptual_hash'] = str(imagehash.average_hash(img))
            except Exception:
                pass
                
        # 3. Audio Fingerprint (Only for audio files)
        if ctx.get('category') == Strings.CAT_AUDIO and pyacoustid:
            try:
                _, fp = pyacoustid.fingerprint_file(fpath)
                ctx['fast_hash'] = fp.decode('utf-8') if isinstance(fp, bytes) else fp
            except Exception:
                pass
                
        # 4. Full Hash (xxHash64)
        if xxhash:
            try:
                hasher = xxhash.xxh64()
                with open(fpath, 'rb') as f:
                    for chunk in iter(partial(f.read, settings.hashing_chunk_size), b""):
                        hasher.update(chunk)
                ctx['full_hash'] = hasher.hexdigest()
            except Exception:
                ctx['full_hash'] = None

    t = threading.Thread(target=_worker, daemon=True)
    t.start()
    t.join(timeout=settings.hashing_timeout)
    
    if t.is_alive():
        # Log timeout if it takes too long
        from ...utils.logger import logger
        logger.warning(f"Hashing timed out for: {ctx['path']} (>{settings.hashing_timeout}s)")
            
    return ctx