class InvalidModeError(Exception):
    """Exception raised when trying to get Mode that is not currently set
        Attributes:
            value -- string that was being tried to be converted
            message -- eplanation of the error
    """

    def __init__(self, mode, message="Got invalid mode from device"):
        self.mode = mode
        self.message = message
        super().__init__(self.message)


class ValueOutOfLimitError(Exception):
    """Exception raised for errors in the input value. Since there apparently exists a firmware bug allowing setting values above limits for resistance and power(see protocol docs) the library will check and limit values itself

    Attributes:
        value -- input value which caused the error
        limit -- the currently set limit
        message -- explanation of the error
    """

    def __init__(self, value, limit, message="Value is above limit"):
        self.value = value
        self.limit = limit
        self.message = message
        super().__init__(self.message)


class NoModeSetError(Exception):
    """Exception raised for trying to set mode that does not support it.

    Attributes:
        mode -- mode that was tried to be set
        message -- explanation of the error
    """

    def __init__(self, mode, message="Mode does not support setting directly from function"):
        self.mode = mode
        self.message = message
        super().__init__(self.message)
