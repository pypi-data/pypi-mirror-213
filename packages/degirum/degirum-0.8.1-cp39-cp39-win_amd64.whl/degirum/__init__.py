#
# DeGirum AI Inference Software Package
# Copyright DeGirum Corp. 2022
#

__version__ = "0.8.1"

import argparse
import logging
import pdb
from urllib.parse import urlparse
from typing import Optional

from .zoo_manager import ZooManager
from .exceptions import DegirumException


logging.getLogger(__name__).addHandler(logging.NullHandler())


def __dir__():
    return [
        "connect",
        "enable_default_logger",
        "aiclient",
        "CoreClient",
        "LOCAL",
        "CLOUD",
    ]


def connect(
    inference_host_address: str,
    zoo_url: Optional[str] = None,
    token: Optional[str] = None,
) -> ZooManager:
    """Connect to the AI inference host and model zoo of your choice.

    This is the main PySDK entry point: you start your work with PySDK by calling this function.

    The following use cases are supported:

    1. You want to perform **cloud inferences** and take models from some **cloud model zoo**.
    2. You want to perform inferences on some **AI server** and take models from some **cloud model zoo**.
    3. You want to perform inferences on some **AI server** and take models from its **local model zoo**.
    4. You want to perform inferences on **local AI hardware** and take models from some **cloud model zoo**.
    5. You want to perform inferences on **local AI hardware** and use **particular model** from your local drive.

    Args:

        inference_host_address: Inference engine designator; it defines which inference engine to use.

            - For AI Server-based inference it can be either the hostname or IP address of the AI Server host, 
            optionally followed by the port number in the form `:port`.

            - For DeGirum Cloud Platform-based inference it is the string `"@cloud"` or [degirum.CLOUD][] constant.

            - For local inference it is the string `"@local"` or [degirum.LOCAL][] constant.

        zoo_url: Model zoo URL string which defines the model zoo to operate with.

            - For a cloud model zoo, it is specified in the following format: `<cloud server prefix>[/<zoo suffix>]`.
            The `<cloud server prefix>` part is the cloud platform root URL, typically `https://cs.degirum.com`.
            The optional `<zoo suffix>` part is the cloud zoo URL suffix in the form `<organization>/<model zoo name>`.
            You can confirm zoo URL suffix by visiting your cloud user account and opening the model zoo management page.
            If `<zoo suffix>` is not specified, then DeGirum public model zoo `degirum/public` is used.


            - For AI Server-based inferences, you may omit both `zoo_url` and `token` parameters. 
            In this case locally-deployed model zoo of the AI Server will be used.

            - For local AI hardware inferences, if you want to use particular AI model from your local drive, then
            you specify `zoo_url` parameter equal to the path to that model's .json configuration file. The `token` 
            parameter is not needed in this case.

        token: Cloud API access token used to access the cloud zoo.

            - To obtain this token you need to open a user account on [DeGirum cloud platform](https://cs.degirum.com). 
            Please login to your account and go to the token generation page to generate an API access token.

    Returns:
        An instance of Model Zoo manager object configured to work with AI inference host and model zoo of your choice.

    Once you created Model Zoo manager object, you may use the following methods:
            
    - [degirum.zoo_manager.ZooManager.list_models][] to list and search models available in the model zoo.
    - [degirum.zoo_manager.ZooManager.load_model][] to create [degirum.model.Model][] model handling object 
    to be used for AI inferences.
    - [degirum.zoo_manager.ZooManager.model_info][] to request model parameters.

    """

    if inference_host_address[0] == "@":

        if inference_host_address == LOCAL:
            #
            # local inference
            #
            if not zoo_url:
                raise DegirumException(
                    "For local inferences, cloud model zoo URL should not be empty"
                )
            elif zoo_url.lower().endswith(".json"):
                # use local model
                return ZooManager(zoo_url)
            else:
                # use cloud model zoo
                url_parsed = urlparse(zoo_url.lower())
                if url_parsed.scheme != "https" and url_parsed.scheme != "http":
                    raise DegirumException(
                        f"For local inferences, cloud model zoo URL '{zoo_url}' should start with "
                        + "https:// or http:// prefix"
                    )

                if not token:
                    raise DegirumException(
                        "For local inferences with cloud zoo, API access token should not be empty"
                    )

                return ZooManager(zoo_url, token)

        elif inference_host_address == CLOUD:
            #
            # cloud inference
            #

            if not zoo_url:
                raise DegirumException(
                    "For cloud inferences, cloud model zoo URL should not be empty"
                )

            if not token:
                raise DegirumException(
                    "For cloud inferences, API access token should not be empty"
                )

            url_parsed = urlparse(zoo_url.lower())
            if url_parsed.scheme == "https":
                scheme = "dgcps://"
            elif url_parsed.scheme == "http":
                scheme = "dgcp://"
            else:
                raise DegirumException(
                    f"For cloud inferences, cloud model zoo URL '{zoo_url}' should start with "
                    + "https:// or http:// prefix"
                )
            port = f":{url_parsed.port}" if url_parsed.port else ""
            cloud_url = f"{scheme}{url_parsed.hostname}{port}{url_parsed.path}"

            return ZooManager(cloud_url, token)

        else:
            raise DegirumException(
                f"Incorrect inference host address '{inference_host_address}'. "
                + f"It should be either {LOCAL}, or {CLOUD}, or a valid AI server address"
            )

    else:
        #
        # AI server inference
        #
        host = inference_host_address.lower()
        if host.find("://") != -1:
            raise DegirumException(
                f"For AI Server inferences, inference host address '{inference_host_address}' should not "
                + "contain any protocol scheme prefix '://'"
            )
        if not zoo_url:
            # use AI server local model zoo
            return ZooManager(inference_host_address)
        else:

            url_parsed = urlparse(zoo_url.lower())
            if url_parsed.scheme != "https" and url_parsed.scheme != "http":
                raise DegirumException(
                    f"For AI server inferences with cloud zoo, cloud model zoo URL '{zoo_url}' should start with "
                    + "https:// or http:// prefix"
                )

            # use cloud model zoo
            if not token:
                raise DegirumException(
                    "For AI server inferences with cloud zoo, API access token should not be empty"
                )
            return ZooManager((inference_host_address, zoo_url), token)


CLOUD: str = "@cloud"
""" Cloud inference designator: 
use it as a first argument of [degirum.connect][] function to specify cloud-based inference """

LOCAL: str = "@local"
""" Local inference designator:
use it as a first argument of [degirum.connect][] function to specify inference on local AI hardware """


def enable_default_logger(
    level: int = logging.DEBUG,
) -> logging.StreamHandler:
    """
    Helper function for adding a StreamHandler to the package logger. Removes any existing handlers.
    Useful for debugging.

    Args:
    
        level: Logging level as defined in logging python package. defaults to logging.DEBUG.

    Returns:

        Returns an instance of added StreamHandler.
    """
    logger = logging.getLogger(__name__)
    logger.handlers = []
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s][%(threadName)s] %(message)s")
    )
    logger.addHandler(handler)
    logger.setLevel(level)
    return handler


def _command_entrypoint(arg_str=None):
    from .server import _server_args, _download_zoo_args
    from ._zoo_accessor import _system_info_args, _trace_args

    parser = argparse.ArgumentParser(description="DeGirum toolkit")

    subparsers = parser.add_subparsers(
        help="use -h flag to see help on subcommands", required=True
    )

    # server subcommand
    subparser = subparsers.add_parser(
        "server",
        description="Manage DeGirum AI server on local host",
        help="manage DeGirum AI server on local host",
    )
    _server_args(subparser)

    # download-zoo subcommand
    subparser = subparsers.add_parser(
        "download-zoo",
        description="Download models from DeGirum cloud model zoo",
        help="download models from DeGirum cloud model zoo",
    )
    _download_zoo_args(subparser)

    # sys-info subcommand
    subparser = subparsers.add_parser(
        "sys-info",
        description="Print system information",
        help="print system information",
    )
    _system_info_args(subparser)

    # trace subcommand
    subparser = subparsers.add_parser(
        "trace",
        description="Manage tracing",
        help="manage tracing",
    )
    _trace_args(subparser)

    # parse args
    args = parser.parse_args(arg_str.split() if arg_str else None)

    # execute subcommand
    args.func(args)


def connect_model_zoo(*args, **kwargs) -> ZooManager:
    """Connect to the model zoo of your choice.
    
    !!! note
        
        This function is deprecated and left only for backward compatibility. Use `connect` instead.

    A _model zoo_ in terminology of PySDK is a collection of AI models and simultaneously an ML inference engine
    type and location.

    The process of creating the PySDK Zoo Accessor object and attaching it to a particular model zoo and, therefore,
    to the inference engine, is called _connecting to a model zoo_.

    Depending on the deployment location, there are several types of model zoos supported by PySDK:

    - Cloud Platform model zoo: inferences are performed by DeGirum Cloud Platform servers; model zoo is
    deployed on DeGirum Cloud Platform.
    - AI server **local** model zoo: inferences are performed by DeGirum AI server running on remote host; model zoo is
    deployed on the same host.
    - AI server **cloud** model zoo: inferences are performed by DeGirum AI server running on remote host, but model zoo is
    deployed on DeGirum Cloud Platform.
    - AI node **local** model zoo: inferences are performed on the local host (node) using AI accelerators installed on
    that node; model zoo is deployed on the local file system of that node.
    - AI node **cloud** model zoo: inferences are performed on the local host (node) using AI accelerators installed on
    that node, but model zoo is deployed on DeGirum Cloud Platform.

    The type of the model zoo is defined by the URL string which you pass as `zoo_url` parameter (see below).

    Keyword Args:

        zoo_url (str): URL string, which defines the model zoo to connect to.
        token (str): Security token string to be passed to the model zoo manager for authentication and authorization.

    !!! note "Note 1"
    
        For DeGirum Cloud Platform connections you need cloud API access token. To obtain this token you need to
        open a user account on [DeGirum cloud platform](https://cs.degirum.com). Please login to your account and
        go to the token generation page to generate API access token.

    !!! note "Note 2"
    
        When dealing with cloud model zoos you specify the cloud zoo URL in the following format:
        `<cloud server URL>[/<zoo URL>]`. The `<cloud server URL>` part is the cloud platform root URL,
        typically `cs.degirum.com`. The optional `<zoo URL>` part is the cloud zoo URL in the form
        `<organization>/<model zoo name>`. You can confirm zoo URL by visiting your cloud user account and opening
        the model zoo management page. If `<zoo URL>` is not specified, then DeGirum public model zoo
        is used.

    The following is an explanation on how to specify `zoo_url` parameter for all supported model zoo types:

    1. You want to perform **cloud inferences** and take models from some **cloud model zoo**.
    
        In this case you specify the `zoo_url` parameter as `"dgcps://<cloud server URL>[/<zoo URL>]"`.
        The `dgcps://` prefix specifies that you want to use cloud inference. It is followed by the cloud zoo URL
        in a format described in the *Note 2* above. Also you specify the `token` parameter equal
        to your API access token.

    2. You want to perform inferences on some **AI server** and take models from its **local model zoo**.

        In this case you specify the `zoo_url` parameter as the hostname or IP address of the AI server machine
        you want to connect to. As a client of the AI server you do not have control on what models are served by
        that AI server -- once the AI server model zoo is deployed, it cannot be changed from the client side unless
        the AI server administrator explicitly updates the model zoo on that AI server.
        The `token` parameter is not needed in this use case.

    3. You want to perform inferences on some **AI server** and take models from some **cloud model zoo**.

        In this case you specify the `zoo_url` parameter as a **tuple**. The first element of this tuple should contain
        the hostname or IP address of the AI server machine you want to connect to. The second element of this tuple
        should contain the cloud model zoo URL in the `"https://<cloud server URL>[/<zoo URL>]"` format, described
        in the *Note 2* above. Also you specify the `token` parameter equal to your API access token.

    4. You want to perform inferences on **local AI hardware** and take models from some **cloud model zoo**.

        In this case you specify the `zoo_url` parameter as `"https://<cloud server URL>[/<zoo URL>]"`.
        The `https://` prefix specifies that you want to use local (not cloud) inference. It is followed by the
        cloud zoo URL in a format described in the *Note 2* above. Also you specify the `token` parameter equal
        to your API access token.

    5. You want to perform inferences on **local AI hardware** and use **particular model** from your local drive.

        In this case you specify `zoo_url` parameter equal to the path to the model .json configuration file.
        The `token` parameter is not needed in this use case.

    !!! note "Note 3"
    
        If you omit `zoo_url` parameter, then the inference will be performed on the local AI hardware and
        models will be taken from DeGirum public cloud model zoo. This is a special case of option 4.
        However, you still need to specify the `token` parameter equal to your API access token.

    Returns:
        An instance of Model Zoo manager object configured to work with AI inference host and model zoo of your choice.
        
    Once you created Model Zoo manager object, you may use the following methods:

    - [degirum.zoo_manager.ZooManager.list_models][] to list and search models available in the model zoo.
    - [degirum.zoo_manager.ZooManager.load_model][] to create [degirum.model.Model][] model handling object to be 
    used for AI inferences.
    - [degirum.zoo_manager.ZooManager.model_info][] to request model parameters.

    """
    return ZooManager(*args, **kwargs)
