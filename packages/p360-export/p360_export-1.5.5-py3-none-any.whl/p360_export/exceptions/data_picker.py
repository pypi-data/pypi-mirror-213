class DataPickerException(Exception):
    pass


class EmptyColumnMappingException(DataPickerException):
    pass


class InvalidFacebookColumnException(DataPickerException):
    pass


class UserIdMappingMissingException(DataPickerException):
    pass


class ClientIdMappingMissingException(DataPickerException):
    pass
