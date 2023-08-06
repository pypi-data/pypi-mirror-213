from __future__ import annotations
import logging, os, re, urllib.request, socket, base64
from types import FunctionType
from urllib.parse import unquote, urlparse
from contextlib import closing
from unittest import TestCase
from ..colors import Colors
from .commons import ProxyConfig, _proxyconfig, report_failure

try:
    from .winhttp import check_winhttp_connectivity
    _with_winhttp = True
except ImportError:
    _with_winhttp = False

try:
    from ..credentials import get_password
    _with_credentials = True
except ImportError:
    _with_credentials = False


logger = logging.getLogger(__name__)

IP_ADDRESS_PATTERN = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")


def check_socket(host, port, timeout=1):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(timeout)
        try:
            returncode = sock.connect_ex((host, port))
            if returncode == 0:
                return True
            else:
                logger.debug("socket connnect_ex returned %d", returncode)
                return False
        except Exception as e:
            logger.debug("socket connnect_ex: %s", e)
            return False


class SimpleProxyHandler(urllib.request.BaseHandler):
    # Inspired from urllib.request.ProxyHandler   
    handler_order = 100 # Proxies must be in front

    def __init__(self, config: ProxyConfig):
        self.config = config

    def finalize(self) -> str:
        # Get proxy url (for logs)
        proxy_logurl = self.config.get_proxy_url(include_password="*")
        logger.debug(f"use proxy for urllib: {proxy_logurl}")

        # Check proxy existency
        if not check_socket(self.config.host, self.config.port):
            logger.warning(f"cannot connect to proxy for urllib: {proxy_logurl}")

        # Prepare usefull variables for add_header and set_proxy
        self.hostport = self.config.hostport
        self.scheme = self.config.scheme

        if self.config.username:
            if not self.config.password:
                if self.config.password_func:
                    raise ValueError(f"password function did not return any value for username: {self.config.username}")
                else:
                    raise ValueError(f"missing password for urllib proxy: {proxy_logurl}")
            userpass = '%s:%s' % (self.config.username, self.config.password)
            self.authorization = "Basic " + base64.b64encode(userpass.encode()).decode("ascii")
        else:
            self.authorization = None

    def http_open(self, req):
        if not req.host:
            return None
        
        if urllib.request.proxy_bypass(req.host):
            # NOTE: because Proxy-Authorization header is not encrypted, we must add it ONLY when we're actually talking to the proxy
            return None

        if not hasattr(self, "authorization"):
            self.finalize()

        if self.authorization:
            req.add_header("Proxy-Authorization", self.authorization)
        req.set_proxy(self.hostport, self.scheme)
        return None
    
    def https_open(self, req):
        return self.http_open(req)


def configure_proxy(url: str = None, exclusions: str = None, password_func: FunctionType = None):
    """
    Configure proxy for urllib requests (and winhttp requests created with `zut.network.winhttp.create_winhttp_request`).
    """
    # Detect proxy URL
    if url is None:
        if "HTTP_PROXY" in os.environ:
            url = os.environ["HTTP_PROXY"]
        elif "http_proxy" in os.environ:
            url = os.environ["http_proxy"]
        elif "HTTPS_PROXY" in os.environ:
            url = os.environ["HTTPS_PROXY"]
        elif "https_proxy" in os.environ:
            url = os.environ["https_proxy"]

    # Detect proxy exclusions
    if exclusions is None:
        if "NO_PROXY" in os.environ:
            exclusions = os.environ["NO_PROXY"]
        elif "no_proxy" in os.environ:
            exclusions = os.environ["no_proxy"]

    # Update proxy configuration
    _proxyconfig.update(url, exclusions=exclusions)
    
    # Detect and register proxy func
    if _proxyconfig.username and not _proxyconfig._password:
        if password_func is None:
            service = os.environ.get("PROXY_PASSWORD_SERVICE", None)
            if service:
                if not _with_credentials:
                    logger.error(f"cannot register PROXY_PASSWORD_SERVICE \"{service}\": zut[credentials] optional dependencies are not installed")
                else:
                    password_func = lambda username: get_password(service, username)
                
        if password_func:
            _proxyconfig.set_password_func(password_func)

    def _del_if_exists(data: dict, attr: str):
        if attr in data:
            del data[attr]

    # Remove environment variables (would take precedence in some cases, which might cause issues: e.g. should contain password or not?)
    _del_if_exists(os.environ, "http_proxy")
    _del_if_exists(os.environ, "https_proxy")
    _del_if_exists(os.environ, "HTTP_PROXY")
    _del_if_exists(os.environ, "HTTPS_PROXY")

    # Ensure no_proxy is specified (must be passed as environment variable for urllib)
    env_exclusions = _proxyconfig.env_exclusions_str
    if env_exclusions:
        os.environ["no_proxy"] = env_exclusions
        os.environ["NO_PROXY"] = env_exclusions
    else:
        _del_if_exists(os.environ, "no_proxy")
        _del_if_exists(os.environ, "NO_PROXY")

    # Stop if no proxy specified/detected
    if not _proxyconfig.host:
        return
    
    # Register proxy for urllib
    try:
        handler = SimpleProxyHandler(_proxyconfig)
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)
    except Exception as e:
        logger.error("cannot register proxy for urllib: %s", e)


def get_configured_proxy_url(for_url: str = None, include_password: bool = False) -> str:
    """
    Return currently configured proxy URL.
    If `for_url` is given, return None if the proxy is excluded for this url.
    """
    if for_url:
        o = urlparse(for_url)
        if urllib.request.proxy_bypass(o.netloc if o.netloc else o.path):
            return None
    return _proxyconfig.get_proxy_url(include_password=include_password)


def get_configured_proxy_hostport(for_url: str = None, include_password: bool = False) -> tuple[str,int]:
    """
    Return currently configured proxy host and port.
    If `for_url` is given, return None if the proxy is excluded for this url.
    """
    if for_url:
        o = urlparse(for_url)
        if urllib.request.proxy_bypass(o.netloc if o.netloc else o.path):
            return None
    return _proxyconfig.host, _proxyconfig.port


def get_configured_proxy_exclusions() -> list[str]:
    """
    Return currently configured proxy exclusions.
    """
    return _proxyconfig.exclusions


def check_urllib_connectivity(url: str, expected_regex: re.Pattern|str, label=None, timeout: float = None, case: TestCase = None) -> bool:
    """
    Check network connectivity using urllib library.
    - `timeout`: in seconds (defaults to 3 seconds).

    Return `True` on success, `False` on failure.
    """        
    if not isinstance(expected_regex, re.Pattern):
        expected_regex = re.compile(expected_regex)

    if label is None:
        label = url

    if not timeout:
        timeout = float(os.environ.get("CHECK_CONNECTIVITY_TIMEOUT", 10))

    msg=f"{label} urllib"

    try:
        res = urllib.request.urlopen(url, timeout=timeout)
        text = res.read().decode('utf-8')
        text_startup = text[0:20].replace('\n', '\\n').replace('\r', '\\r') + ('…' if len(text) > 20 else '')
        
        if not expected_regex.match(text):
            report_failure(case, f"{msg}: response ({Colors.RED}{text_startup}{Colors.RESET}) does not match expected regex ({Colors.GRAY}{expected_regex.pattern}{Colors.RESET}")
            return False

        logger.info(f"{msg}: {Colors.GREEN}success{Colors.RESET} (response: {Colors.GRAY}{text_startup}{Colors.RESET})")
        return True
    except urllib.error.URLError as e:
        report_failure(case, f"{msg}: {Colors.RED}{e.reason}{Colors.RESET}")
        return False


def check_connectivity(url: str, expected_regex: re.Pattern|str, label=None, timeout: float = None, case: TestCase = None) -> bool:
    """
    Check network connectivity with urllib library, and winhttp library on Windows (if [winhttp] extra dependencies are installed).
    - `timeout`: in seconds (defaults to 3 seconds).

    Return `True` on success, `False` on failure.
    """ 
    ok = check_urllib_connectivity(url, expected_regex, label=label, timeout=timeout, case=case)

    if _with_winhttp:
        ok = ok and check_winhttp_connectivity(url, expected_regex, label=label, timeout=timeout, case=case)

    return ok
