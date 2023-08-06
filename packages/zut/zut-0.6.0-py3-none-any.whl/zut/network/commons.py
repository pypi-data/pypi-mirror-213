from __future__ import annotations
import re, logging
from types import FunctionType
from urllib.parse import quote, unquote, urlparse
from unittest import TestCase

logger = logging.getLogger(__name__)


def report_failure(case: TestCase, msg: str):
    if case:
        case.fail(msg)
    else:
        logger.error(msg)


class ProxyConfig:
    def __init__(self):
        self.clear()

    def clear(self):
        self.host: str = None
        self.port: int = None
        self.username: str = None
        self.password_func: FunctionType = None
        self.scheme: str = "http"
        self.exclusions: list[str] = None

        # caches
        self._non_cidr_exclusions_str = '__undefined__'
        self._password: str = None

    def update(self, url: str, exclusions: str|list[str] = None):
        self.clear()
        if url is None:
            return

        o = urlparse(url)
        m = re.match(r"^(?:(?P<username>[^\:]+)(?:\:(?P<password>[^\:]+))?@)?(?P<host>[^@\:]+)\:(?P<port>\d+)$", o.netloc)
        if not m:
            raise ValueError("invalid url netloc \"%s\"" % o.netloc)

        self.host = unquote(m.group("host")) if m.group("host") else None
        self.port = int(m.group("port"))
        self.username = unquote(m.group("username")) if m.group("username") else None
        self._password = unquote(m.group("password")) if m.group("password") else None
        self.scheme = o.scheme

        if exclusions is not None:
            if isinstance(exclusions, str):
                self.exclusions = exclusions.split(',')
            else:
                self.exclusions = exclusions

    def set_password_func(self, func: FunctionType):
        self.password_func = func

    @property
    def is_rtm_host(self):
        return self.host.endswith(('.rtm.fr','.rtm.lan'))

    @property
    def hostport(self):
        if not self.host:
            return None
        return f"{self.host}:{self.port}"

    @property
    def env_exclusions_str(self) -> str:
        """
        Return a comma-separated string of exclusions, for use as an environment variable.
        """
        if not self.exclusions:
            return None
        return ",".join(self.exclusions)

    @property
    def non_cidr_exclusions_str(self) -> str:
        """
        Return a comma-separated string of exclusions, excluding CIDR blocks (not supported by WinHTTP).
        """
        if self._non_cidr_exclusions_str == '__undefined__':
            if self.exclusions:
                self._non_cidr_exclusions_str = ",".join([exclusion for exclusion in self.exclusions if not "/" in exclusion])
            else:
                logger.warning("no exclusions for proxy: missing NO_PROXY environment variable?")
                self._non_cidr_exclusions_str = "localhost"

        return self._non_cidr_exclusions_str

    @property
    def password(self):
        if self._password is None:
            if self.username and self.password_func:
                self._password = self.password_func(self.username)

        return self._password

    def get_proxy_url(self, include_password=False):
        if self.host is None:
            return None
        
        proxy_url = self.scheme + "://"

        if self.username:
            proxy_url += quote(self.username)

            if include_password:
                if self.password:
                    if include_password == "*":
                        proxy_url += ":" + ("*" * len(self.password))
                    else:
                        proxy_url += ":" + quote(self.password)
            
            proxy_url += "@"

        proxy_url += f"{quote(self.host)}:{self.port}"
        return proxy_url


_proxyconfig = ProxyConfig()
