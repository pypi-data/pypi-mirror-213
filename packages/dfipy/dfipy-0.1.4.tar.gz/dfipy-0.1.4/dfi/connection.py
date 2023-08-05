"""
Class to connect to the DFI server.
"""

# TODO: investigate if it is possible to merge DFIConnect and DFIGet in a single class.


class DFIConnect:
    """
    Class instantiating the connectors to the DFI API.

    Parameters
    ----------
    api_token: str,
        token provided by generalsystem.com to access the running DFI environments.
    instance_name: str,
        DFI API engine instance.
    namespace: str,
        Name of the space where the DFI instance lives.
    query_timeout: int = 60,
        Time after an unresponsive query will be dropped.
    base_url : str =None
        Base url where the service is located
    env: str = "Prod"
        Either "Prod" or "Dev".
    progress_bar: bool = False
        Visualise a progress bar if True (slows down the execution but useful for demos and tests).

    Examples
    --------
    >>> dfi_conn = dfi.DFIConnect(api_token=api_token, namespace=namespace, instance_name=instance_name)
    >>> dfi_conn.streaming_headers
    """

    def __init__(
        self,
        api_token: str,
        instance_name: str,
        namespace: str = None,
        query_timeout: int = 60,
        base_url: str = None,
        env: str = "Prod",
        progress_bar: bool = False,
    ) -> None:
        self._api_token = api_token
        if base_url is None:
            if env == "Prod":
                self._base_url = "https://api.dataflowindex.io"
            if env == "Dev":
                self._base_url = "https://api.dfi.dev.excession.co"
        else:
            self._base_url = base_url
        self._query_timeout = query_timeout
        self._streaming_headers = {
            "X-API-TOKEN": f"Bearer {api_token}",
            "accept": "text/event-stream",
        }
        self._synchronous_headers = {
            "X-API-TOKEN": f"Bearer {api_token}",
            "accept": "application/json",
            "content-type": "application/json",
        }
        self._namespace = namespace
        self._instance_name = instance_name
        self._progress_bar = progress_bar
        if namespace is None:
            self._qualified_instance_name = instance_name
        else:
            self._qualified_instance_name = f"{namespace}.{instance_name}"

    def __repr__(self):
        return f"{self.__class__.__name__} {self.__dict__}"

    def __str__(self):
        return f"""DFIConnection instance with base_url={self.base_url},
                   query_timeout={self.query_timeout}, streaming_headers={self.streaming_headers},
                   synchronous_headers={self.synchronous_headers}, namespace={self.namespace}"""

    # Getter and setter for api_token
    @property
    def api_token(self):
        return self._api_token

    @api_token.setter
    def api_token(self, value):
        self._api_token = value

    # Getter and setter for progress_bar
    @property
    def progress_bar(self):
        return self._progress_bar

    @progress_bar.setter
    def progress_bar(self, value):
        self._progress_bar = value

    # Getter and setter for query_timeout
    @property
    def query_timeout(self):
        return self._query_timeout

    @query_timeout.setter
    def query_timeout(self, value):
        self._query_timeout = value

    # Getter and setter for streaming_headers
    @property
    def streaming_headers(self):
        return self._streaming_headers

    @streaming_headers.setter
    def streaming_headers(self, value):
        self._streaming_headers = value

    # Getter and setter for synchronous_headers
    @property
    def synchronous_headers(self):
        return self._synchronous_headers

    @synchronous_headers.setter
    def synchronous_headers(self, value):
        self._synchronous_headers = value

    # Getter and setter for namespace
    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, value):
        self._namespace = value

    # Getter and setter for instance_name
    @property
    def instance_name(self):
        return self._instance_name

    @instance_name.setter
    def instance_name(self, value):
        self._instance_name = value

    # Getter and setter for base_url
    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value

    # Getter and setter for qualified_instance_name
    @property
    def qualified_instance_name(self):
        return self._qualified_instance_name

    @qualified_instance_name.setter
    def qualified_instance_name(self, value):
        self._qualified_instance_name = value
