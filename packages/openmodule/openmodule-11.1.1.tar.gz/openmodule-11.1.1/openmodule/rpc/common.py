import warnings


def channel_to_response_topic(channel: str) -> str:
    # TODO: backwards compatibiltiy, remove in version 12
    if isinstance(channel, bytes):
        warnings.warn('\n\nPassing channel as bytes is deprecated. Please pass as strings.\n',
                      DeprecationWarning, stacklevel=2)
        channel = channel.decode("utf8")
    return "rpc-rep-" + channel


def channel_to_request_topic(channel: str) -> str:
    # TODO: backwards compatibiltiy, remove in version 12
    if isinstance(channel, bytes):
        warnings.warn('\n\nPassing channel as bytes is deprecated. Please pass as strings.\n',
                      DeprecationWarning, stacklevel=2)
        channel = channel.decode("utf8")
    return "rpc-req-" + channel
