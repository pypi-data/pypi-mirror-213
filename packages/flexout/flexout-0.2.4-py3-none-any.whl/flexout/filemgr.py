"""
File manager.

Optional requirement for Samba/Windows shares: pip install smbprotocol
"""
from __future__ import annotations
import os, ntpath, sys, logging, shutil
from pathlib import Path
from enum import Enum

try:
    import smbclient
    import smbclient.path as smbclient_path
    import smbclient.shutil as smbclient_shutil
except ImportError:
    smbclient = None
    smbclient_path = None
    smbclient_shutil = None

_cache = {
    'smb_credentials': False
}

logger = logging.getLogger('__name__')



def configure_smb_credentials(user: str = None, password: str = None):
    if user or password:
        if not smbclient:
            logger.warning(f'ignore smb credentials: package `smbprotocol` not available')
        else:
            smbclient.ClientConfig(username=user, password=password)
            _cache['smb_credentials'] = True


def can_use_network_paths():
    if sys.platform == 'win32' and not _cache['smb_credentials']:
        return True  # Python is natively compatible with Samba shares on Windows

    return smbclient is not None


def _standardize(path: str) -> tuple[str,bool]:
    """
    Return (path, native).
    """
    if not path:
        return path, True
    
    if isinstance(path, Path):
        path = str(path)

    path = os.path.expanduser(path)
    
    if not (path.startswith("\\\\") or path.startswith("//")):
        return path, True  # not a network path
        
    if sys.platform == 'win32' and not _cache['smb_credentials']:
        return path, True  # Python is natively compatible with Samba shares on Windows

    return path, False


def dirname(path: str):
    path, native = _standardize(path)
    
    if native:
        return os.path.dirname(path)
    
    return ntpath.dirname(path)


def basename(path: str):
    path, native = _standardize(path)

    if native:
        return os.path.basename(path)

    return ntpath.basename(path)
    

def splitext(path: str):
    path, native = _standardize(path)

    if native:
        return os.path.splitext(path)
    
    return ntpath.splitext(path)


def exists(path: str):
    path, native = _standardize(path)

    if native:
        return os.path.exists(path)

    if not smbclient:
        raise ModuleNotFoundError(f'missing package `smbprotocol`')
    return smbclient_path.exists(path)


def stat(path: str):
    path, native = _standardize(path)

    if native:
        return os.stat(path)
    
    if not smbclient:
        raise ModuleNotFoundError(f'missing package `smbprotocol`')
    return smbclient.stat(path)


def makedirs(path: str, exist_ok: bool = False):
    path, native = _standardize(path)

    if native:
        return os.makedirs(path, exist_ok=exist_ok)

    if not smbclient:
        raise ModuleNotFoundError(f'missing package `smbprotocol`')
    return smbclient.makedirs(path, exist_ok=exist_ok)


def remove(path: str):
    path, native = _standardize(path)

    if native:
        return os.remove(path)

    if not smbclient:
        raise ModuleNotFoundError(f'missing package `smbprotocol`')
    return smbclient.remove(path)


def rmtree(path: str, ignore_errors=False, onerror=None):
    path, native = _standardize(path)

    if not native:
        return shutil.rmtree(path, ignore_errors=ignore_errors, onerror=onerror)
    
    if not smbclient_shutil:
        raise ModuleNotFoundError(f'missing package `smbprotocol`')
    return smbclient_shutil.rmtree(path, ignore_errors=ignore_errors, onerror=onerror)


def open_file(path: str, mode="r", buffering: int = -1, encoding: str = None, errors: str = None, newline: str = None, mkdir: bool = False, **kwargs):
    if mkdir:
        dir_path = dirname(path)
        if dir_path:
            makedirs(dir_path, exist_ok=True)

    path, native = _standardize(path)

    if native:
        return open(path, mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline, **kwargs)

    if not smbclient:
        raise ModuleNotFoundError(f'missing package `smbprotocol`')
    return smbclient.open_file(path, mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline, **kwargs)


def read_bytes(path: str):
    """
    Open the file in bytes mode, read it, and close the file.
    """
    path, native = _standardize(path)

    if native:
        return Path(path).read_bytes()
    
    if not smbclient:
        raise ModuleNotFoundError(f'missing package `smbprotocol`')
    with smbclient.open_file(path, mode='rb') as f:
        return f.read()


def read_text(path: str, encoding: str = None, errors: str = None):
    """
    Open the file in text mode, read it, and close the file.
    """
    path, native = _standardize(path)

    if native:
        return Path(path).read_text(encoding=encoding, errors=errors)
    
    if not smbclient:
        raise ModuleNotFoundError(f'missing package `smbprotocol`')
    with smbclient.open_file(path, mode='r', encoding=encoding, errors=errors) as f:
        return f.read()


def write_bytes(path: str, data):
    """
    Open the file in bytes mode, write to it, and close the file.
    """
    path, native = _standardize(path)

    if native:
        return Path(path).write_bytes(data)
    
    if not smbclient:
        raise ModuleNotFoundError(f'missing package `smbprotocol`')
    with smbclient.open_file(path, mode='wb') as f:
        return f.write(data)


def write_text(path: str, data: str, encoding: str = None, errors: str = None, newline: str = None):
    """
    Open the file in text mode, write to it, and close the file.
    """
    path, native = _standardize(path)

    if native:
        return Path(path).write_text(data, encoding=encoding, errors=errors, newline=newline)

    if not smbclient:
        raise ModuleNotFoundError(f'missing package `smbprotocol`')
    with smbclient.open_file(path, mode='w', encoding=encoding, errors=errors, newline=newline) as f:
        return f.write(data)


def copy(src: str, dst: str, follow_symlinks=True):
    src, src_native = _standardize(src)
    dst, dst_native = _standardize(dst)
    
    if src_native and dst_native:
        return shutil.copy(src, dst, follow_symlinks=follow_symlinks)
    
    if not smbclient_shutil:
        raise ModuleNotFoundError(f'missing package `smbprotocol`')
    return smbclient_shutil.copy(src, dst, follow_symlinks=follow_symlinks)


def copy2(src: str, dst: str, follow_symlinks=True):
    src, src_native = _standardize(src)
    dst, dst_native = _standardize(dst)
    
    if src_native and dst_native:
        return shutil.copy2(src, dst, follow_symlinks=follow_symlinks)
    
    if not smbclient_shutil:
        raise ModuleNotFoundError(f'missing package `smbprotocol`')
    return smbclient_shutil.copy2(src, dst, follow_symlinks=follow_symlinks)


def copyfile(src: str, dst: str, follow_symlinks=True):
    src, src_native = _standardize(src)
    dst, dst_native = _standardize(dst)
    
    if src_native and dst_native:
        return shutil.copyfile(src, dst, follow_symlinks=follow_symlinks)
    
    if not smbclient_shutil:
        raise ModuleNotFoundError(f'missing package `smbprotocol`')
    return smbclient_shutil.copyfile(src, dst, follow_symlinks=follow_symlinks)


def copystat(src: str, dst: str, follow_symlinks=True):
    src, src_native = _standardize(src)
    dst, dst_native = _standardize(dst)
    
    if src_native and dst_native:
        return shutil.copystat(src, dst, follow_symlinks=follow_symlinks)
    
    if not smbclient_shutil:
        raise ModuleNotFoundError(f'missing package `smbprotocol`')
    return smbclient_shutil.copystat(src, dst, follow_symlinks=follow_symlinks)


def copymode(src: str, dst: str, follow_symlinks=True):
    src, src_native = _standardize(src)
    dst, dst_native = _standardize(dst)

    if src_native and dst_native:
        return shutil.copytree(src, dst, follow_symlinks=follow_symlinks)

    if not smbclient_shutil:
        raise ModuleNotFoundError(f'missing package `smbprotocol`')
    return smbclient_shutil.copymode(src, dst, follow_symlinks=follow_symlinks)


def copytree(src: str, dst: str, symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=False):
    src, src_native = _standardize(src)
    dst, dst_native = _standardize(dst)

    if src_native and dst_native:
        return shutil.copytree(src, dst, symlinks=symlinks, ignore=ignore, ignore_dangling_symlinks=ignore_dangling_symlinks, dirs_exist_ok=dirs_exist_ok)

    if not smbclient_shutil:
        raise ModuleNotFoundError(f'missing package `smbprotocol`')
    return smbclient_shutil.copytree(src, dst, symlinks=symlinks, ignore=ignore, ignore_dangling_symlinks=ignore_dangling_symlinks, dirs_exist_ok=dirs_exist_ok)
