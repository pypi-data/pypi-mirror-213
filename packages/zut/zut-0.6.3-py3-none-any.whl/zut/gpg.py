from __future__ import annotations
import subprocess, logging
from tempfile import TemporaryDirectory
from pathlib import Path
from .process import check_completed_subprocess
from .network import get_configured_proxy_url

logger = logging.getLogger(__name__)


def download_gpg_key(keyid: str, target_path: Path, keyserver: str = None, include_proxy_password: bool = False):
    with TemporaryDirectory() as tmpdir:
        # Retrieve the key
        cmd = ["gpg", "--homedir", tmpdir]
        
        if keyserver:
            cmd += ["--keyserver", keyserver]
            
            if keyserver.startswith("hkp://"):
                proxy_url = get_configured_proxy_url(keyserver, include_password=include_proxy_password)
                if proxy_url:
                    cmd += ["--keyserver-options", f"http-proxy={proxy_url}"]

        cmd += ["--recv-keys", keyid]
        subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Export the key
        cmd = ["gpg", "--homedir", tmpdir, "--output", target_path, "--export", keyid]
        subprocess.run(cmd, capture_output=True, text=True, check=True)


def verify_gpg_signature(sign_path: Path, public_key_path: Path):
    cmd = ["gpg", "--no-default-keyring", "--keyring", public_key_path, "--verify", sign_path]
    cp = subprocess.run(cmd, capture_output=True, text=True)
    
    if cp.returncode != 0:
        check_completed_subprocess(cp, logger, label='gpg verify')
        return False
    
    return True
