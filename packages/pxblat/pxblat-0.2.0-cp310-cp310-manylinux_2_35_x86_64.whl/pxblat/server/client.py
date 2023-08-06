import tempfile
from pathlib import Path
from threading import Thread
from typing import Optional

from pxblat.extc import ClientOption
from pxblat.extc import pygfClient
from pxblat.parser import read

from .basic import wait_server_ready
from .server import ServerOption


def create_client_option():
    """
    Creates a new ClientOption object with default values.

    Return:
        ClientOption object

    """
    return ClientOption()


def _resolve_host_port(
    client_option: ClientOption, host: Optional[str], port: Optional[int]
):
    """Resolves the host and port for the client option.

    Args:
        client_option: ClientOption object
        host: Optional[str]
        port: Optional[int]
    """
    if host is not None:
        client_option.hostName = host

    if port is not None:
        client_option.portName = str(port)

    if not client_option.hostName and not client_option.portName:
        raise ValueError("host and port are both empty")


def query_server(
    option: ClientOption,
    host: Optional[str] = None,
    port: Optional[int] = None,
    seqname: Optional[str] = None,
    parse: bool = True,
):
    """
    Sends a query to the server and returns the result.

    Args:
        option: ClientOption object
        host: Optional[str]
        port: Optional[int]
        seqname: Optional[str]
        parse: bool

    Returns:
        str or bytes: The result of the query.

    """
    _resolve_host_port(option, host, port)

    fafile = None
    if not option.inName and not option.inSeq:
        raise ValueError("inName and inSeq are both empty")

    if option.inSeq:
        fafile = tempfile.NamedTemporaryFile(mode="w", delete=False)

        seqname = fafile.name if seqname is None else seqname
        fafile.write(f">{seqname}\n")
        fafile.write(option.inSeq)
        fafile.close()

        option.inName = fafile.name

    # return bytes
    ret = pygfClient(option)

    try:
        ret_decode = ret.decode().rsplit(",\n", 1)[0]  # type: ignore
    except UnicodeDecodeError:
        ret_decode = ret.decode("latin-1").rsplit(",\n", 1)[0]  # type: ignore

    if fafile is not None:
        Path(fafile.name).unlink()

    if parse and ret_decode:
        return read(ret_decode, "psl")

    return ret_decode


class Client(Thread):
    def __init__(
        self,
        option: ClientOption,
        host: Optional[str] = None,
        port: Optional[int] = None,
        wait_ready: bool = False,
        wait_timeout: int = 60,
        server_option: Optional[ServerOption] = None,
        seqname: Optional[str] = None,
        parse: bool = True,
        daemon: bool = True,
    ):
        """A class for querying a gfServer using a separate thread.

        Args:
            option: ClientOption object
            host: Optional[str]
            port: Optional[int]
            wait_ready: bool
            wait_timeout: int
            server_option: Optional[ServerOption]
            seqname: Optional[str]
            parse: bool
            daemon: bool

        Attributes:
            result: The result of the query.

        """
        super().__init__(daemon=daemon)
        self.option = option
        self._host = host
        self._port = port
        self._resolve_host_port()

        self._wait_ready = wait_ready
        self._wait_timeout = wait_timeout
        self._server_option = server_option
        self._seqname = seqname
        self._parse = parse

        self.result = None

    def run(self):
        if self._wait_ready:
            wait_server_ready(
                self.host,
                self.port,
                timeout=self._wait_timeout,
                gfserver_option=self._server_option,
            )

        ret = query_server(self.option, seqname=self._seqname, parse=self._parse)

        self.result = ret

    def get(self):
        self.join()
        return self.result

    @property
    def host(self):
        if self._host is None:
            return self.option.hostName

        return self._host

    @host.setter
    def host(self, value: str):
        self._host = value

    @property
    def port(self):
        if self._port is None:
            return int(self.option.portName)

        return self._port

    @port.setter
    def port(self, value: int):
        self._port = value

    @classmethod
    def create_option(cls):
        """
        Creates a new ClientOption object with default values.

        Return:
            ClientOption object

        """
        return create_client_option()

    def _resolve_host_port(self):
        _resolve_host_port(self.option, self._host, self._port)
