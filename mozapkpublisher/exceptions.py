import logging

logger = logging.getLogger(__name__)


class LoggedError(Exception):
    def __init__(self, msg):
        logger.fatal(msg)
        super(LoggedError, self).__init__(msg)


class WrongArgumentGiven(LoggedError):
    pass


class CheckSumMismatch(LoggedError):
    def __init__(self, checked_file, expected, actual):
        super(CheckSumMismatch, self).__init__(
            msg='Downloading "{}" failed!. Checksum "{}" was expected, but actually got "{}"'
                .format(checked_file, expected, actual)
        )


class NoTransactionError(Exception):
    def __init__(self, package_name):
        super(NoTransactionError, self).__init__(
            'Transaction has not been started for package "{}"'.format(package_name)
        )
