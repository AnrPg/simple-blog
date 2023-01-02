

class ValidationError(Exception):
    def __init__(self, error_message: str, status_code: int):
        super().__init__(error_message)

        self.error_message = error_message
        self.status_code = status_code

class MalformedFullName(ValidationError):
    def __init__(self, error_message: str, status_code: int, firstname_present: bool, lastname_present: bool) -> None:
        super().__init__(error_message, status_code)
        self.firstname_present = firstname_present
        self.lastname_present = lastname_present

class MissingIdentifier(ValidationError):
    def __init__(self, error_message: str, status_code: int) -> None:
        super().__init__(error_message, status_code)
        self.error_message = error_message
        self.status_code = status_code

class MalformedTelephone(ValidationError):
    def __init__(self, error_message: str, status_code: int) -> None:
        super().__init__(error_message, status_code)
        self.error_message = error_message
        self.status_code = status_code

class MalformedDate(ValidationError):
    def __init__(self, error_message: str, status_code: int) -> None:
        super().__init__(error_message, status_code)
        self.error_message = error_message
        self.status_code = status_code