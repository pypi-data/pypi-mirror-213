__all__ = ('JSONRPCHeaders',)


class JSONRPCHeaders:
    """List of JSONRPC request / response headers."""

    AUTHORIZATION = 'Authorization'
    CONTENT_TYPE_HEADER = 'Content-Type'
    USER_AGENT = 'User-Agent'

    APP_ID_HEADER = 'App-Id'
    SERVER_ID_HEADER = 'Server-Id'
    CORRELATION_ID_HEADER = 'Correlation-Id'

    REQUEST_DEADLINE_HEADER = 'Deadline'
    REQUEST_TIMEOUT_HEADER = 'Timeout'
    RETRIES = 'RPC-Retries'
    CALLBACK_ID = 'RPC-Callback'
    ABORT_ON_ERROR = 'RPC-Batch-Abort-Error'
    USE_TEMPLATE = 'RPC-Batch-Template'

    SESSION_ID_HEADER = 'Session-Id'
