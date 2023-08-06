from __future__ import annotations

import os
import subprocess
import sys
from argparse import ArgumentParser
from datetime import datetime
from getpass import getpass


if sys.platform == "win32":
    import win32cred
    from keyring.backends.Windows import WinVaultKeyring

    # See: https://docs.microsoft.com/en-us/windows/win32/api/wincred/ns-wincred-credentiala
    CRED_TYPE_GENERIC = 1 # The credential is a generic credential. The credential will not be used by any particular authentication package. The credential will be stored securely but has no other significant characteristics.
    CRED_TYPE_DOMAIN_PASSWORD = 2 # The credential is a password credential and is specific to Microsoft's authentication packages. The NTLM, Kerberos, and Negotiate authentication packages will automatically use this credential when connecting to the named target.
    CRED_TYPE_DOMAIN_CERTIFICATE = 3 # The credential is a certificate credential and is specific to Microsoft's authentication packages. The Kerberos, Negotiate, and Schannel authentication packages automatically use this credential when connecting to the named target.

    enumerate_additional_props = ["LastWritten", "TargetAlias", "Comment", "Type", "Flags", "CredentialBlob"]
    ENUMERATE_HEADERS = ["Service", "Username", *enumerate_additional_props]

    def enumerate_credentials(service=None, username=None):
        if service is not None:
            service = service.lower()
        if username is not None:
            username = username.lower()
        
        for cred in win32cred.CredEnumerate():
            cred_service = cred["TargetName"]
            cred_username = cred["UserName"]

            # Filter
            if service is not None:
                if not service in cred_service.lower():
                    continue
            if username is not None:
                if cred_username is None or not username in cred_username.lower():
                    continue

            # Additional properties
            props = []
            for prop in enumerate_additional_props:
                if prop == "CredentialBlob":
                    props.append("X" if cred[prop] else "")
                elif prop == "Type":
                    indication = ""
                    if cred["Type"] == CRED_TYPE_GENERIC:
                        indication = "generic"
                    elif cred["Type"] == CRED_TYPE_DOMAIN_PASSWORD:
                        indication = "domain password"
                    elif cred["Type"] == CRED_TYPE_DOMAIN_CERTIFICATE:
                        indication = "domain certificate"
                    props.append(str(cred[prop]) + (" (%s)" % indication if indication else ""))
                else:
                    props.append(cred[prop])

            yield [cred_service, cred_username, *props]
    

    def get_username(service):
        found = None

        for cred in win32cred.CredEnumerate():
            if cred["Type"] == CRED_TYPE_GENERIC and cred["TargetName"] == service and cred["UserName"]:
                if found:
                    raise ValueError(f"several usernames found for service {service}")
                found = cred["UserName"]

        if not found:
            return None
        
        return found


    _keyring = None

    def _get_keyring():
        global _keyring
        if _keyring is None:
            _keyring = WinVaultKeyring()
        return _keyring

    def get_password(service, username = None):
        return _get_keyring().get_password(service, username if username else '')


    def set_password(service, username, password):
        return _get_keyring().set_password(service, username, password)


    def delete_password(service, username):
        return _get_keyring().delete_password(service, username)


else: # sys.platform != "win32"
    import re
    from glob import glob

    _several_slashes_re = re.compile(r"/{2,}")

    def _sanitize_part(part):
        """ Replace several slashes with only one """
        if not part:
            return part
        part = part.replace("://", ":")
        return _several_slashes_re.sub("/", part)
        
    def _get_key(service, username):
        if not service:
            raise ValueError(f'service name must be provided')
        
        parts = [_sanitize_part(service)]
        if username:
            parts.append(_sanitize_part(username))

        return os.path.join(*parts).rstrip("/")
    
    ENUMERATE_HEADERS = ["Service", "Username", "LastWritten", "Path"]

    def enumerate_credentials(service=None, username=None):
        if service is not None:
            service = _sanitize_part(service.lower())
        if username is not None:
            username = _sanitize_part(username.lower())

        prefix = os.path.expanduser("~/.password-store/")
        for path in glob(f"{prefix}**/*.gpg", recursive=True):
            name_without_extension = path[:-4]
            name_parts = name_without_extension[len(prefix):].rsplit("/", 1)
            if len(name_parts) == 0:             
                cred_service = ""
                cred_username = ""
            elif len(name_parts) == 1:                
                cred_service = name_parts[0]
                cred_username = ""
            else:
                cred_service = "/".join(name_parts[:-1])
                cred_username = name_parts[-1]

            # Filter
            if service is not None:
                if not service in cred_service.lower():
                    continue
            if username is not None:
                if cred_username or not username in cred_username.lower():
                    continue

            last_written = datetime.fromtimestamp(os.path.getmtime(path))
            yield [cred_service, cred_username, last_written, path]

        
    def get_username(service):
        found = None

        service = _sanitize_part(service)
        for cred in enumerate_credentials():
            if cred[0] == service and cred[1]:
                if found:
                    raise ValueError(f"several usernames found for service {service}")
                found = cred[1]

        if not found:
            return None
        
        return found

    
    _not_in_the_password_store_re = re.compile(r"^Error: .+ is not in the password store.$")
    def get_password(service, username = None):
        key = _get_key(service, username)
        try:
            cp = subprocess.run(["pass", "show", key], capture_output=True, check=True, text=True)
        except subprocess.CalledProcessError as err:
            if cp.returncode == 1 and _not_in_the_password_store_re.match(cp.stderr):
                return None
            else:
                raise err
        return cp.stdout.splitlines()[0]


    def set_password(service, username, password):
        if not service:
            raise ValueError("service cannot be empty")

        password = password.splitlines()[0]
        inp = '%s\n' % password
        inp *= 2
        
        key = _get_key(service, username)
        subprocess.run(['pass', 'insert', '--force', key], input=inp, capture_output=True, check=True, text=True)


    def delete_password(service, username):
        key = _get_key(service, username)
        subprocess.run(['pass', 'rm', '--force', key], check=True, capture_output=True)


def add_arguments(parser: ArgumentParser):
    parser.add_argument("action", nargs="?", choices=["list", "ls", "get", "set", "delete", "del", "rm"], default="list", help="action to perform")
    parser.add_argument("service", nargs="?", help="service name")
    parser.add_argument("username", nargs="?", help="user name")


def handle(action: str = None, service: str = None, username: str = None):
    """
    List, get or set credentials from the credentials manager.
    """    
    if action == "get":
        # Get a credential
        if not service:
            service = input("Service: ")
        if not username:
            username = input(f"Username for service \"{service}\": ")
        print(get_password(service, username))

    elif action == "set":
        # Set a credential
        if not service:
            service = input("Service: ")
        if not username:
            username = input(f"Username for service \"{service}\": ")
        set_password(service, username, getpass(f"Password for service \"{service}\" (username: \"{username}\"): "))

    elif action in ["delete", "del", "rm"]:
        # Delete a credential
        if not service:
            service = input("Service: ")
        if not username:
            username = input(f"Username for service \"{service}\": ")
        delete_password(service, username)

    else: # list
        from tabulate import tabulate

        # Search/list available credentials
        if sys.platform == "win32":
            print("See: rundll32.exe keymgr.dll, KRShowKeyMgr")
        else:
            print("See: find ~/.password-store -type f -name '*.gpg'")
            
        rows = []
        for cred in enumerate_credentials(service=service, username=username):
            rows.append(cred)

        rows.sort(key=lambda row: row[0].lower())

        # Display LastWritten as simplified local time
        try:
            i = ENUMERATE_HEADERS.index("LastWritten")            
            for row in rows:
                localdt = row[i].astimezone()
                row[i] = localdt.strftime("%H:%M" if localdt.date() == datetime.now().date() else "%Y-%m-%d")

        except ValueError:
            pass


        print(tabulate(rows, ENUMERATE_HEADERS))
